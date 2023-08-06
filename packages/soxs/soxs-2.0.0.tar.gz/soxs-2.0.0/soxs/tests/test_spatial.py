from soxs.spatial import PointSourceModel, BetaModel, \
    AnnulusModel
from soxs.spectra import ApecGenerator, ConvolvedSpectrum
import numpy as np
import os
import shutil
import tempfile
import astropy.io.fits as pyfits
from astropy.units import Quantity
from soxs.events import write_radial_profile, make_exposure_map
from soxs.simput import SimputCatalog
from soxs.instrument import instrument_simulator, sigma_to_fwhm, \
    AuxiliaryResponseFile
from soxs.instrument_registry import get_instrument_from_registry, \
    add_instrument_to_registry
from sherpa.astro.ui import set_source, freeze, \
    fit, covar, get_covar_results, set_covar_opt, \
    load_data, set_stat, set_method

kT = Quantity(6.0, "keV")
Z = 0.3
redshift = 0.03
norm = 1.0e-3
nH = 0.04
exp_time = Quantity(50.0, "ks")
area = Quantity(3.0, "m**2")

prng = 31

agen = ApecGenerator((0.05, "keV"), (12.0, "keV"), 10000, broadening=True)
spec = agen.get_spectrum(kT, Z, redshift, norm)
spec.apply_foreground_absorption(nH)

ra0 = 30.0
dec0 = 45.0

def test_point_source():
    tmpdir = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(tmpdir)

    pt_src_pos = PointSourceModel(ra0, dec0)
    sim_cat = SimputCatalog.from_models("pt_src", "pt_src", spec, pt_src_pos,
                                        exp_time, area, prng=prng)
    sim_cat.write_catalog(overwrite=True)

    inst = get_instrument_from_registry("hdxi")
    inst["name"] = "hdxi_big_psf"
    inst["psf"] = ["gaussian", 5.0]

    add_instrument_to_registry(inst)

    instrument_simulator("pt_src_simput.fits", "pt_src_evt.fits", exp_time,
                         "hdxi_big_psf", [ra0, dec0], ptsrc_bkgnd=False, 
                         instr_bkgnd=False, foreground=False, prng=prng)

    psf_scale = inst["psf"][1]
    dtheta = inst["fov"]*60.0/inst["num_pixels"]

    f = pyfits.open("pt_src_evt.fits")
    x = f["EVENTS"].data["X"]
    y = f["EVENTS"].data["Y"]
    f.close()

    scalex = np.std(x)*sigma_to_fwhm*dtheta
    scaley = np.std(y)*sigma_to_fwhm*dtheta

    assert (scalex - psf_scale)/psf_scale < 0.01
    assert (scaley - psf_scale)/psf_scale < 0.01

    os.chdir(curdir)
    shutil.rmtree(tmpdir)

def test_annulus():

    tmpdir = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(tmpdir)

    r_in = 10.0
    r_out = 30.0

    ann_pos = AnnulusModel(ra0, dec0, r_in, r_out)

    sim_cat = SimputCatalog.from_models("ann", "ann", spec, ann_pos,
                                        exp_time, area, prng=prng)
    sim_cat.write_catalog(overwrite=True)

    instrument_simulator("ann_simput.fits", "ann_evt.fits", exp_time,
                         "hdxi", [ra0, dec0], ptsrc_bkgnd=False, 
                         instr_bkgnd=False, foreground=False, prng=prng)

    inst = get_instrument_from_registry("hdxi")
    arf = AuxiliaryResponseFile(inst["arf"])
    cspec = ConvolvedSpectrum(spec, arf)
    ph_flux = cspec.get_flux_in_band(0.5, 7.0)[0].value
    S0 = ph_flux/(np.pi*(r_out**2-r_in**2))

    write_radial_profile("ann_evt.fits", "ann_evt_profile.fits", [ra0, dec0],
                         1.1*r_in, 0.9*r_out, 100, ctr_type="celestial", 
                         emin=0.5, emax=7.0, overwrite=True)

    load_data(1, "ann_evt_profile.fits", 3, ["RMID","SUR_BRI","SUR_BRI_ERR"])
    set_stat("chi2")
    set_method("levmar")
    set_source("const1d.src")
    src.c0 = 0.8*S0

    fit()
    set_covar_opt("sigma", 1.645)
    covar()
    res = get_covar_results()

    assert np.abs(res.parvals[0]-S0) < res.parmaxes[0]

    os.chdir(curdir)
    shutil.rmtree(tmpdir)

def test_beta_model():
    tmpdir = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(tmpdir)

    prng = 32

    r_c = 20.0
    beta = 1.0

    exp_time = Quantity(500.0, "ks")

    beta_src_pos = BetaModel(ra0, dec0, r_c, beta)
    sim_cat = SimputCatalog.from_models("beta", "beta", spec, beta_src_pos,
                                        exp_time, area, prng=prng)
    sim_cat.write_catalog(overwrite=True)

    instrument_simulator("beta_simput.fits", "beta_evt.fits", exp_time,
                         "hdxi", [ra0, dec0], ptsrc_bkgnd=False, 
                         instr_bkgnd=False, foreground=False, prng=prng)

    inst = get_instrument_from_registry("hdxi")
    arf = AuxiliaryResponseFile(inst["arf"])
    cspec = ConvolvedSpectrum(spec, arf)
    ph_flux = cspec.get_flux_in_band(0.5, 7.0)[0].value
    S0 = 3.0*ph_flux/(2.0*np.pi*r_c*r_c)

    write_radial_profile("beta_evt.fits", "beta_evt_profile.fits", [ra0, dec0],
                         0.0, 100.0, 200, ctr_type="celestial", emin=0.5, 
                         emax=7.0, overwrite=True)

    load_data(1, "beta_evt_profile.fits", 3, ["RMID","SUR_BRI","SUR_BRI_ERR"])
    set_stat("chi2")
    set_method("levmar")
    set_source("beta1d.src")
    src.beta = 1.0
    src.r0 = 10.0
    src.ampl = 0.8*S0
    freeze(src.xpos)

    fit()
    set_covar_opt("sigma", 1.645)
    covar()
    res = get_covar_results()

    assert np.abs(res.parvals[0]-r_c) < res.parmaxes[0]
    assert np.abs(res.parvals[1]-beta) < res.parmaxes[1]
    assert np.abs(res.parvals[2]-S0) < res.parmaxes[2]

    os.chdir(curdir)
    shutil.rmtree(tmpdir)

def test_beta_model_flux():
    tmpdir = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(tmpdir)

    r_c = 20.0
    beta = 1.0

    prng = 34

    beta_src_pos = BetaModel(ra0, dec0, r_c, beta)
    sim_cat = SimputCatalog.from_models("beta", "beta", spec, beta_src_pos,
                                        exp_time, area, prng=prng)
    sim_cat.write_catalog(overwrite=True)

    instrument_simulator("beta_simput.fits", "beta_evt.fits", exp_time,
                         "acisi_cy0", [ra0, dec0], ptsrc_bkgnd=False,
                         instr_bkgnd=False, foreground=False, 
                         roll_angle=37.0, prng=prng)

    ph_flux = spec.get_flux_in_band(0.5, 7.0)[0].value
    S0 = 3.0*ph_flux/(2.0*np.pi*r_c*r_c)

    wspec = spec.new_spec_from_band(0.5, 7.0)

    make_exposure_map("beta_evt.fits", "beta_expmap.fits", wspec.emid.value,
                      weights=wspec.flux.value, overwrite=True)

    write_radial_profile("beta_evt.fits", "beta_evt_profile.fits", [ra0, dec0],
                         0.0, 100.0, 200, ctr_type="celestial", emin=0.5,
                         emax=7.0, expmap_file="beta_expmap.fits", overwrite=True)

    load_data(1, "beta_evt_profile.fits", 3, ["RMID","SUR_FLUX","SUR_FLUX_ERR"])
    set_stat("chi2")
    set_method("levmar")
    set_source("beta1d.src")
    src.beta = 1.0
    src.r0 = 10.0
    src.ampl = 0.8*S0
    freeze(src.xpos)

    fit()
    set_covar_opt("sigma", 1.645)
    covar()
    res = get_covar_results()

    assert np.abs(res.parvals[0]-r_c) < res.parmaxes[0]
    assert np.abs(res.parvals[1]-beta) < res.parmaxes[1]
    assert np.abs(res.parvals[2]-S0) < res.parmaxes[2]

    os.chdir(curdir)
    shutil.rmtree(tmpdir)

if __name__ == "__main__":
    test_point_source()
    test_annulus()
    test_beta_model()
    test_beta_model_flux()