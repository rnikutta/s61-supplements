"""Plotting routines for (some) figures used in Agliozzo et al. (2016), MNRAS, [TODO: insert final DOI here]

   Some of these plot routines require that you have rhocube.py and
   models.py present in the same directory.

   Get RHOCUBE from github:

     https://github.com/rnikutta/rhocube/

   or best clone directly:

     git clone https://github.com/rnikutta/rhocube

"""

__author__  = "Robert Nikutta, Claudia Agliozzo"
__version__ = "20161115"  # yyyymmdd

from astropy.io import fits
import numpy as N
import pylab as p
import matplotlib.ticker as ticker
import models  # this will also import rhocube.py


def plot_fig6_MassLossRateHistogram(nefile='s61-TNS-17GHz-model-3-6-rw-chi33.fits',\
                                    v=27.,\
                                    epsmin=1e-7,\
                                    savefile='s61_17GHzmasslossrate.pdf'):

    """Mass-loss rate as function of time.

    Parameters
    ----------

    nefile : str
        Name of fits file with 3D model cube of electron density n_e (cm^-3)
        Defaults here to the best-fit (maximum-a-posteriori, MAP) truncated normal shell model.

    v : float
        Shell expansion velocity in km/s

    epsmin : float
        Tiny float to use for zero-ing random fluctuations caused by
        ndimage.shift(), if any.

    savefile : str or None
        If string, the name of the file to save the figure to.

    Returns
    -------

    Nothing.

    Example
    -------

    .. code-block:: python

        import plots
        plots.fig6_masslossrate_histogram()

    """
    
    from scipy import ndimage

    # DATA AND CUBE
    
    # load header and rho array from model file
    rho = fits.getdata(nefile)
    header = fits.getheader(nefile)
    pixelscale = header['CDELT1']
    npix = header['NAXIS1']
    xoff = header['XOFF']
    yoff = header['YOFF']

    # re-center the shell to (x,y,z)=(0,0,0); note the inverse order of x,y,z indices from scipy to fits
    # Note that this is via cubic spline interpolation; can cause very small value fluctuations.
    rho = ndimage.shift(rho,(0,-yoff/pixelscale,-xoff/pixelscale))  # shifting by (fractional) pixels
    
    # compute distance array R (all in units of integer pixel)
    x = N.arange(npix)-npix/2
    X,Y,Z = N.meshgrid(x,x,x)
    R = N.sqrt(X**2+Y**2+Z**2)

    # compute mass in shells of thickness 1 pixel
    dMs = N.zeros(npix/2)   # will hold mass in a shell of radius r & thickness 1 pixel
    for j in xrange(dMs.size-1):
        co = (R>j) & (R<=(j+1))
        if j == 0:  # include central pixel
            co = co | (R==0)
        dM = (rho[co]).sum()
        dMs[j] = dM

    # PHYSICS
    
    # constants / conversions
    mproton = 1.672621777e-27  # kg
    Msun = 1.98855e30          # kg
    pc2cm = 3.0857e18          # parsec in cm
    pc2km = 3.0857e13          # pc in kilometers
    y2s = 365*24*60*60.        # seconds in one year

    voxel2Msun = (pixelscale * pc2cm)**3 * mproton/Msun
    dMs = dMs * voxel2Msun
    
    # PLOT
    rmids = N.linspace(0.,pixelscale*(npix/2),npix/2)
    yearsmids = rmids / ((v / pc2km) * y2s)  # convert radii to years using expansion velocity
    xvals = yearsmids

    dyears = N.diff(yearsmids)[0]
    yvals = dMs/dyears
    yvals[yvals<epsmin] = 0.  # get rid of tiny fluctuations introduced by ndimage.shift()

    # peak of mass-loss at epoch...
    idx = yvals.argmax()
    print "The peak of mass-loss rate (%.3e Msun/yr) occured %d years ago." % (yvals[idx],xvals[idx])

    # make figure and plot
    fig = p.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)

    # plot histogram
    ax.plot(-xvals,yvals,'b-',drawstyle='steps',linewidth=2, color='black') # negative as in "time in the past"

    # format and beautify the figure
    ax.set_xlabel(r'${\rm time\ (yr)}$',fontsize=16)
    ax.set_ylabel(r' ${\rm \dot M\ (M_\odot\ yr^{-1})}$ ',fontsize=16)
    ax.yaxis.get_major_formatter().set_powerlimits((-6, -5))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5000))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1000))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.000002))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.000001))
    ax.grid()
    ax.set_xlim(-25000,0)
    ax.legend(['17-GHz data TNS model'],loc=0)
    
    # save figure
    savefigure(fig,savefile)

    # sanity checks
    print "\nSanity checks"
    print "Sum of voxel masses = ", (rho * voxel2Msun).sum()
    print "Sum of shell masses = ", dMs.sum(), " <-- They should be the same."



def plot_figA1_gallery(cmap='Blues_r',savefile='rhocube_gallery.png'):

    """Plot gallery of several RHOCUBE models. Pretty.

    Parameters
    ----------
    cmap : str
        Valid name of matplotlib colormap to use. Default 'Blues_r'.

    savefile : str or None
        If string, the name of the file to save the figure to.

    Returns
    -------

    Nothing.

    Example
    -------

    .. code-block:: python

        import plots
        plots.plot_figA1_gallery()

    """
    
    # globals
    fontsize = 10
    extent = (-1,1,-1,1)
    cmap_ = p.cm.get_cmap(cmap)

    # plot single panel
    def plot_panel(ax,data,xlabel='x',ylabel=None,panellabel=None,title=''):

        print "Panel: ", panellabel
        
        ax.imshow(data.image.T,origin='lower',extent=extent,cmap=cmap_,interpolation='none')
        ax.set_title(title)
        ax.set_xlabel('x')

        if ylabel is not None:
            ax.set_ylabel('y')
        
        if panellabel is not None:
            ax.text(0.1,0.1,panellabel,color='w',transform=ax.transAxes)
        
        return ax

    # figure setup
    p.rcParams['axes.labelsize'] = fontsize
    p.rcParams['font.size'] =  fontsize
    p.rcParams['legend.fontsize'] = fontsize
    p.rcParams['xtick.labelsize'] = fontsize
    p.rcParams['ytick.labelsize'] = fontsize

    # don't use Type 3 fonts (requirement by MNRAS)
    p.rcParams['ps.useafm'] = True
    p.rcParams['pdf.use14corefonts'] = True
    p.rcParams['text.usetex'] = True
    p.rcParams['font.family'] = 'sans-serif'
    p.rcParams['text.latex.preamble'] = [
        r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
        r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
    ] 

    fig = p.figure(figsize=(17,3.1))

    # plot the panels
    ax = fig.add_subplot(161)
    mod = models.PowerLawShell(201,smoothing=1.)
    mod(*(0.4,0.8,0,0,None))
    ax = plot_panel(ax,mod,ylabel='y',panellabel='(a)',title='Constant-density shell')

    ax = fig.add_subplot(162)
    mod = models.TruncatedNormalShell(201,smoothing=1.)
    mod(*(0.5,0.1,0.3,1.,0,0,None))
    ax = plot_panel(ax,mod,panellabel='(b)',title='Truncated Normal shell')

    ax = fig.add_subplot(163)
    mod = models.ConstantDensityTorus(201,smoothing=1.)
    mod(*(0.6,0.25,0,0,35,45,None))
    ax = plot_panel(ax,mod,panellabel='(c)',title='Constant-density torus')

    ax = fig.add_subplot(164)
    mod = models.ConstantDensityDualCone(201,smoothing=1.)
    mod(*(0.8,45,30,50,0,0,None))
    ax = plot_panel(ax,mod,panellabel='(d)',title='Constant-density dual cone')

    ax = fig.add_subplot(165)
    mod = models.Helix3D(101,smoothing=1.,envelope='dualcone')
    mod(*(0.7,1,0.17,0,0,-90,0,0,None))
    ax = plot_panel(ax,mod,panellabel='(e)',title='Helix on dual cone')

    ax = fig.add_subplot(166)
    mod = models.Helix3D(101,smoothing=1.,envelope='cylinder')
    mod(*(0.6,1,0.17,0,0,-90,0,0,None))
    ax = plot_panel(ax,mod,panellabel='(f)',title='Helix on cylinder')
    
    # figure adjustments
    p.subplots_adjust(left=0.04,right=0.99,bottom=0.06,top=0.987,wspace=0.3)

    # save figure
    savefigure(fig,savefile)


def savefigure(fig,savefile):
    """Generic figure saving.

    Parameters
    ----------
    fig : instance
        Instance of figure (from pylab) to be saved to savefile.

    savefile : str or None
        If string, the name of the file to save the figure to.

    """
    
    if savefile is not None:
        print "Writing figure to file %s" % savefile
        fig.savefig(savefile)
        print "Done."


