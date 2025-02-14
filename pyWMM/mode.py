# ---------------------------------------------------------------------------- #
#
# ---------------------------------------------------------------------------- #
'''





'''

# ---------------------------------------------------------------------------- #
#
# ---------------------------------------------------------------------------- #
from pyWMM import WMM as wmm
import numpy as np
from scipy import interpolate
from scipy import integrate
from matplotlib import pyplot as plt

# ---------------------------------------------------------------------------- #
#
# ---------------------------------------------------------------------------- #

'''
   general mode
'''
class Mode:

    def __init__(self, beta, center, wavelength, waveguideWidth = None, waveguideThickness = None,
                 coreEps = None ,claddingEps = None, Eps = None,
                 Ex = None, Ey = None, Ez = None, Er = None, Ephi = None,
                 Hx = None, Hy = None, Hz = None, Hr = None, Hphi = None,
                 x = None, y = None, r = None, radius = None,
                 pol = None, neff = None, rc = 0
                 ):

        #Initialize all the other variables
        self.omega = 2 * np.pi * wmm.C0 / (wavelength*1e-6)
        self.wavelength = wavelength
        self.beta = beta
        self.pol  = None
        self.sym  = None
        self.k0   = None
        self.neff = None
        self.radius = radius
        self.waveguideWidth = waveguideWidth
        self.waveguideThickness = waveguideThickness
        self.claddingEps = claddingEps
        self.coreEps = coreEps
        self.rc = 0

        # Set waveguide's center
        self.xCenter = center[0]
        self.yCenter = center[1]
        self.zCenter = center[2]

        # Ensure the correct coordinate system
        if (Ex is None and Er is None and Ez is None and Ephi is None) or (Hx is None and Hr is None and Hz is None and Hphi is None) or (x is None and r is None):
            raise ValueError('Missing either an x component or r component in fields!')
        elif Ex is None and Hx is None and x is None:
            self.coordinates = wmm.CYLINDRICAL
        elif Er is None and Hr is None and r is None:
            self.coordinates = wmm.CARTESIAN
        else:
            raise ValueError('Invalid coordinate system defined!')

        if self.coordinates == wmm.CYLINDRICAL and radius == None:
            raise ValueError('Failed to specify the waveguide\'s center radius!')

        # Interpolate all of the fields on the given grid
        self.y = y
        self.total_power = 1
        if self.coordinates == wmm.CARTESIAN:
            #self.Eps_r          = interpolate.RectBivariateSpline(x, y, np.real(Eps))
            #self.Eps_i          = interpolate.RectBivariateSpline(x, y, np.imag(Eps))

            self.Ex_ro           = interpolate.RectBivariateSpline(x, y, np.real(Ex))
            self.Ex_io           = interpolate.RectBivariateSpline(x, y, np.imag(Ex))
            self.Ex_r = lambda r,y,grid=True: self.Ex_ro(r,y,grid=grid) / np.sqrt(self.total_power)
            self.Ex_i = lambda r,y,grid=True: self.Ex_io(r,y,grid=grid) / np.sqrt(self.total_power)

            self.Ey_ro           = interpolate.RectBivariateSpline(x, y, np.real(Ey))
            self.Ey_io           = interpolate.RectBivariateSpline(x, y, np.imag(Ey))
            self.Ey_r = lambda r,y,grid=True: self.Ey_ro(r,y,grid=grid) / np.sqrt(self.total_power)
            self.Ey_i = lambda r,y,grid=True: self.Ey_io(r,y,grid=grid) / np.sqrt(self.total_power)

            self.Ez_ro           = interpolate.RectBivariateSpline(x, y, np.real(Ez))
            self.Ez_io           = interpolate.RectBivariateSpline(x, y, np.imag(Ez))
            self.Ez_r = lambda r,y,grid=True: self.Ez_ro(r,y,grid=grid) / np.sqrt(self.total_power)
            self.Ez_i = lambda r,y,grid=True: self.Ez_io(r,y,grid=grid) / np.sqrt(self.total_power)

            self.Hx_ro           = interpolate.RectBivariateSpline(x, y, np.real(Hx))
            self.Hx_io           = interpolate.RectBivariateSpline(x, y, np.imag(Hx))
            self.Hx_r = lambda r,y,grid=True: self.Hx_ro(r,y,grid=grid) / np.sqrt(self.total_power)
            self.Hx_i = lambda r,y,grid=True: self.Hx_io(r,y,grid=grid) / np.sqrt(self.total_power)

            self.Hy_ro           = interpolate.RectBivariateSpline(x, y, np.real(Hy))
            self.Hy_io           = interpolate.RectBivariateSpline(x, y, np.imag(Hy))
            self.Hy_r = lambda r,y,grid=True: self.Hy_ro(r,y,grid=grid) / np.sqrt(self.total_power)
            self.Hy_i = lambda r,y,grid=True: self.Hy_io(r,y,grid=grid) / np.sqrt(self.total_power)

            self.Hz_ro           = interpolate.RectBivariateSpline(x, y, np.real(Hz))
            self.Hz_io           = interpolate.RectBivariateSpline(x, y, np.imag(Hz))
            self.Hz_r = lambda r,y,grid=True: self.Hz_ro(r,y,grid=grid) / np.sqrt(self.total_power)
            self.Hz_i = lambda r,y,grid=True: self.Hz_io(r,y,grid=grid) / np.sqrt(self.total_power)

            self.x            = x
        elif self.coordinates == wmm.CYLINDRICAL:
            #self.Eps_r          = interpolate.RectBivariateSpline(r, y, np.real(Eps))
            #self.Eps_i          = interpolate.RectBivariateSpline(r, y, np.imag(Eps))

            self.Er_ro           = interpolate.RectBivariateSpline(r, y, np.real(Er))
            self.Er_io           = interpolate.RectBivariateSpline(r, y, np.imag(Er))
            self.Er_r = lambda r,y,grid=True: self.Er_ro(r,y,grid=grid) / np.sqrt(self.total_power)
            self.Er_i = lambda r,y,grid=True: self.Er_io(r,y,grid=grid) / np.sqrt(self.total_power)

            self.Ey_ro           = interpolate.RectBivariateSpline(r, y, np.real(Ey))
            self.Ey_io           = interpolate.RectBivariateSpline(r, y, np.imag(Ey))
            self.Ey_r = lambda r,y,grid=True: self.Ey_ro(r,y,grid=grid) / np.sqrt(self.total_power)
            self.Ey_i = lambda r,y,grid=True: self.Ey_io(r,y,grid=grid) / np.sqrt(self.total_power)

            self.Ephi_ro         = interpolate.RectBivariateSpline(r, y, np.real(Ephi))
            self.Ephi_io         = interpolate.RectBivariateSpline(r, y, np.imag(Ephi))
            self.Ephi_r = lambda r,y,grid=True: self.Ephi_ro(r,y,grid=grid) / np.sqrt(self.total_power)
            self.Ephi_i = lambda r,y,grid=True: self.Ephi_io(r,y,grid=grid) / np.sqrt(self.total_power)

            self.Hr_ro           = interpolate.RectBivariateSpline(r, y, np.real(Hr))
            self.Hr_io           = interpolate.RectBivariateSpline(r, y, np.imag(Hr))
            self.Hr_r = lambda r,y,grid=True: self.Hr_ro(r,y,grid=grid) / np.sqrt(self.total_power)
            self.Hr_i = lambda r,y,grid=True: self.Hr_io(r,y,grid=grid) / np.sqrt(self.total_power)

            self.Hy_ro           = interpolate.RectBivariateSpline(r, y, np.real(Hy))
            self.Hy_io           = interpolate.RectBivariateSpline(r, y, np.imag(Hy))
            self.Hy_r = lambda r,y,grid=True: self.Hy_ro(r,y,grid=grid) / np.sqrt(self.total_power)
            self.Hy_i = lambda r,y,grid=True: self.Hy_io(r,y,grid=grid) / np.sqrt(self.total_power)

            self.Hphi_ro         = interpolate.RectBivariateSpline(r, y, np.real(Hphi))
            self.Hphi_io         = interpolate.RectBivariateSpline(r, y, np.imag(Hphi))
            self.Hphi_r = lambda r,y,grid=True: self.Hphi_ro(r,y,grid=grid) / np.sqrt(self.total_power)
            self.Hphi_i = lambda r,y,grid=True: self.Hphi_io(r,y,grid=grid) / np.sqrt(self.total_power)

            self.r            = r
        else:
            raise ValueError('Invalid coordinate system defined!')

        # Get the power of the modes
        self.TE_power = self.calc_TE_power()
        self.TM_power = self.calc_TM_power()
        self.total_power = self.calc_total_power()

        # Get the normalizing factor
        self.nrm    = 1
        #self.ampfac = np.sqrt(self.nrm)/np.sqrt(self.total_power)
        #self.ampfac = 1

    def Eps(self,x=0,y=0,z=0,grid=True,centering=True):
        if centering:
            x = x-self.xCenter
            y = y-self.yCenter
            z = z-self.zCenter
        if self.coordinates == wmm.CARTESIAN:
            X,Y,Z = np.meshgrid(x,y,z,indexing='ij')
            epsFunc = np.ones((x.size,y.size,z.size)) * self.claddingEps
            if self.rc == 0:
                coreIndex = ((X >= -self.waveguideWidth/2) & (X < self.waveguideWidth/2)
                        & (Y >= -self.waveguideThickness/2) & (Y < self.waveguideThickness/2))
            else:
                coreIndex = (2*np.abs(X)/self.waveguideWidth) ** (self.waveguideWidth/self.rc) + (2*np.abs(Y)/(self.waveguideThickness)) ** (self.waveguideThickness/self.rc) <= 1
            epsFunc[coreIndex] = self.coreEps
            return np.squeeze(epsFunc)
            '''
            if z is np.ndarray:
                return np.squeeze(np.tile(self.Eps_r(x,y,grid=grid) + 1j*self.Eps_i(x,y,grid=grid),(1,z.size)))
            else:
                return self.Eps_r(x,y,grid=grid) + 1j*self.Eps_i(x,y,grid=grid)
            '''
        elif self.coordinates == wmm.CYLINDRICAL:
            X,Y,Z = np.meshgrid(x,y,z,indexing='ij')
            R = np.sqrt(X ** 2 + Z ** 2) - self.radius
            epsFunc = np.ones((x.size,y.size,z.size)) * self.claddingEps
            coreIndex = ((R >= -self.waveguideWidth/2) & (R < self.waveguideWidth/2)
                    & (Y >= -self.waveguideThickness/2) & (Y < self.waveguideThickness/2))
            epsFunc[coreIndex] = self.coreEps
            return np.squeeze(epsFunc)

    def Ex(self,x,y,z=0,grid=True,centering=True):
        if centering:
            x = x-self.xCenter
            y = y-self.yCenter
            z = z-self.zCenter
        if self.coordinates == wmm.CARTESIAN:
            if z.size > 1:
                z = np.reshape(z,(1,-1))
            return (self.Ex_r(x,y,grid=grid) + 1j*self.Ex_i(x,y,grid=grid)) * \
                np.exp(-1j*self.beta*z)

        elif self.coordinates == wmm.CYLINDRICAL:
            X,Y,Z = np.meshgrid(x,y,z,sparse=True, indexing='ij')
            R     = np.sqrt(X ** 2 + Z ** 2) - self.radius
            phi   = np.arctan2(Z,X)
            temp  = np.squeeze(
            (np.cos(phi) * (self.Er_r(R,Y,grid=False) + self.Er_i(R,Y,grid=False)) -
             np.sin(phi) * (self.Ephi_r(R,Y,grid=False) + self.Ephi_i(R,Y,grid=False)) )
            * np.exp(-1j*self.beta*self.radius*phi))
            return temp

    def Ey(self,x,y,z=0,grid=True,centering=True):
        if centering:
            x = x-self.xCenter
            y = y-self.yCenter
            z = z-self.zCenter
        if self.coordinates == wmm.CARTESIAN:
            if z is np.ndarray:
                z = np.reshape(z,(1,-1))
            return (self.Ey_r(x,y,grid=grid) + 1j*self.Ey_i(x,y,grid=grid)) * \
                np.exp(-1j*self.beta*z)
        elif self.coordinates == wmm.CYLINDRICAL:
            X,Y,Z = np.meshgrid(x,y,z,sparse=True, indexing='ij')
            phi = np.arctan2(Z,X)
            R = np.sqrt(X ** 2 + Z ** 2) - self.radius
            temp = np.squeeze((self.Ey_r(R,Y,grid=False) + 1j*self.Ey_i(R,Y,grid=False))
                     * np.exp(-1j*self.beta*self.radius*phi))
            return temp

    def Ez(self,x,y,z=0,grid=True,centering=True):
        if centering:
            x = x-self.xCenter
            y = y-self.yCenter
            z = z-self.zCenter
        if self.coordinates == wmm.CARTESIAN:
            if z is np.ndarray:
                z = np.reshape(z,(1,-1))
            return (self.Ez_r(x,y,grid=grid) + 1j*self.Ez_i(x,y,grid=grid)) * \
                np.exp(-1j*self.beta*z)
        elif self.coordinates == wmm.CYLINDRICAL:
            #Ez = Hrow * cos(phi) - Hphi * sin(phi)
            X,Y,Z = np.meshgrid(x,y,z,sparse=True, indexing='ij')
            phi = np.arctan2(Z,X)
            R = np.sqrt(X ** 2 + Z ** 2) - self.radius
            temp = np.squeeze(
            ((np.sin(phi)) * (self.Er_r(R,Y,grid=False) + self.Er_i(R,Y,grid=False)) +
             (np.cos(phi)) * (self.Ephi_r(R,Y,grid=False) + self.Ephi_i(R,Y,grid=False)) )
            * np.exp(-1j*self.beta*self.radius*phi))
            return temp

    def Hx(self,x,y,z=0,grid=True,centering=True):
        if centering:
            x = x-self.xCenter
            y = y-self.yCenter
            z = z-self.zCenter
        if self.coordinates == wmm.CARTESIAN:
            if z is np.ndarray:
                z = np.reshape(z,(1,-1))
            return (self.Hx_r(x,y,grid=grid) + 1j*self.Hx_i(x,y,grid=grid)) * \
                np.exp(-1j*self.beta*z)
        elif self.coordinates == wmm.CYLINDRICAL:
            X,Y,Z = np.meshgrid(x,y,z,sparse=True, indexing='ij')
            R = np.sqrt(X ** 2 + Z ** 2) - self.radius
            phi = np.arctan2(Z,X)
            temp = np.squeeze(
            ((np.cos(phi)) * (self.Hr_r(R,Y,grid=False) + self.Hr_i(R,Y,grid=False)) -
             (np.sin(phi)) * (self.Hphi_r(R,Y,grid=False) + self.Hphi_i(R,Y,grid=False)) )
            * np.exp(-1j*self.beta*self.radius*phi))
            return temp

    def Hy(self,x,y,z=0,grid=True,centering=True):
        if centering:
            x = x-self.xCenter
            y = y-self.yCenter
            z = z-self.zCenter
        if self.coordinates == wmm.CARTESIAN:
            if z is np.ndarray:
                z = np.reshape(z,(1,-1))
            return (self.Hy_r(x,y,grid=grid) + 1j*self.Hy_i(x,y,grid=grid)) * \
                np.exp(-1j*self.beta*z)
        elif self.coordinates == wmm.CYLINDRICAL:
            X,Y,Z = np.meshgrid(x,y,z,sparse=True, indexing='ij')
            R = np.sqrt(X ** 2 + Z ** 2) - self.radius
            phi = np.arctan2(Z,X)
            temp = np.squeeze((self.Hy_r(R,Y,grid=False) + 1j*self.Hy_i(R,Y,grid=False))
                              * np.exp(-1j*self.beta*self.radius*phi))
            return temp

    def Hz(self,x,y,z=0,grid=True,centering=True):
        if centering:
            x = x-self.xCenter
            y = y-self.yCenter
            z = z-self.zCenter
        if self.coordinates == wmm.CARTESIAN:
            if z is np.ndarray:
                z = np.reshape(z,(1,-1))
            return (self.Hz_r(x,y,grid=grid) + 1j*self.Hz_i(x,y,grid=grid)) * \
                np.exp(-1j*self.beta*z)
        elif self.coordinates == wmm.CYLINDRICAL:
            #Ez = Hrow * cos(phi) - Hphi * sin(phi)
            X,Y,Z = np.meshgrid(x,y,z,sparse=True, indexing='ij')
            R = np.sqrt(X ** 2 + Z ** 2) - self.radius
            phi = np.arctan2(Z,X)
            temp = np.squeeze(
            ((np.sin(phi)) * (self.Hr_r(R,Y,grid=False) + self.Hr_i(R,Y,grid=False)) +
             (np.cos(phi)) * (self.Hphi_r(R,Y,grid=False) + self.Hphi_i(R,Y,grid=False)) )
            * np.exp(-1j*self.beta*self.radius*phi))
            return temp


    def get_field(self, fComp, x, y, z):
        #Extract center
        centerX = self.center[0]
        centerY = self.center[1]
        centerZ = self.center[2]

        if fComp == wmm.E:
            if self.coordinates == wmm.CYLINDRICAL:
                r = np.sqrt((x - centerX) ** 2 + (z - centerZ) ** 2)
                Er   = self.Er(r,(y-centerY))
                Ey   = self.Ey(r,(y-centerY))
                Ephi = self.Ephi(r,(y-centerY))
                Ex   = Er * np.sin(Ephi)
                Ez   = Er * np.cos(Ephi)
            else:
                Ex = self.Ex((x-centerX),(y-centerY))
                Ey = self.Ey((x-centerX),(y-centerY))
                Ez = self.Ez((x-centerX),(y-centerY))
            E = np.squeeze(np.array([Ex,Ey,Ez]) * self.ampfac)
            return E
        elif fComp == wmm.H:
            if self.coordinates == wmm.CYLINDRICAL:
                r = np.sqrt((x - centerX) ** 2 + (z - centerZ) ** 2)
                Hr   = self.Hr(r,(y-centerY))
                Hy   = self.Hy(r,(y-centerY))
                Hphi = self.Hphi(r,(y-centerY))
                Hx   = Hr * np.sin(Hphi)
                Hz   = Hr * np.cos(Hphi)
            else:
                Hx = self.Hx((x-centerX),(y-centerY))
                Hy = self.Hy((x-centerX),(y-centerY))
                Hz = self.Hz((x-centerX),(y-centerY))
            H = np.squeeze(np.array([Hx,Hy,Hz]) * self.ampfac)
            return H
        elif fComp == wmm.Eps:
            if self.coordinates == wmm.CYLINDRICAL:
                r = np.sqrt((x - centerX) ** 2 + (z - centerZ) ** 2)
                Eps = self.Eps(r,(y-centerY))
            else:
                Eps = np.squeeze(self.Eps((x-centerX),(y-centerY)))
            return Eps
        else:
            raise ValueError("Invalid component specified!")

	# longitudinal component of the Poyntingvector,
	# integrated over the entire x-y-domain
	# TE part
    def calc_TE_power(self):
        if self.coordinates == wmm.CARTESIAN:
            f = lambda y, x: (self.Ey_r(x,y) + self.Ey_i(x,y)) *\
                    (self.Hx_r(x,y) + self.Hx_i(x,y)).conj()
            xmin = self.x[0]; xmax = self.x[-1];
        elif self.coordinates == wmm.CYLINDRICAL:
            f = lambda y, r: (self.Ey_r(r,y) + self.Ey_i(r,y)) *\
                    (self.Hr_r(r,y) + self.Hr_i(r,y)).conj()
            xmin = self.r[0]; xmax = self.r[-1];
        else:
            raise ValueError('Invalid coordinate system defined!')
        ymin = self.y[0]; ymax = self.y[-1];

        intResults = wmm.complex_quadrature(f, xmin, xmax, ymin, ymax)
        return -0.5 * intResults

	# longitudinal component of the Poyntingvector,
	# integrated over the entire x-y-domain
	# TM part
    def calc_TM_power(self):
        if self.coordinates == wmm.CARTESIAN:
            f = lambda y, x: (self.Ex_r(x,y) + self.Ex_i(x,y)) *\
                    (self.Hy_r(x,y) + self.Hy_i(x,y)).conj()
            xmin = self.x[0]; xmax = self.x[-1];
        elif self.coordinates == wmm.CYLINDRICAL:
            f = lambda y, r: (self.Er_r(r,y) + self.Er_i(r,y)) *\
                    (self.Hy_r(r,y) + self.Hy_i(r,y)).conj()
            xmin = self.r[0]; xmax = self.r[-1];
        else:
            raise ValueError('Invalid coordinate system defined!')
        ymin = np.min(self.y); ymax = np.min(self.y[-1]);

        intResults = wmm.complex_quadrature(f, xmin, xmax, ymin, ymax)
        return 0.5 * intResults

    def calc_total_power(self):
        return np.abs(np.real(self.calc_TM_power() + self.calc_TM_power()))

    def getPhasor(self,z):
        z = z-self.zCenter
        if self.coordinates == wmm.CARTESIAN:
            return np.exp(-1j*self.beta*z)
        elif self.coordinates == wmm.CYLINDRICAL:
            if np.abs(z) > self.radius:
                theta = 0
            else:
                theta = np.pi/2 - np.arccos(z/self.radius)
            return np.exp(-1j*self.beta*self.radius*theta)
        else:
            raise ValueError('Invalid coordinate system!')
