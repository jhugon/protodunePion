#!/usr/bin/evn python

import math
import numpy
from matplotlib import pyplot as plt

MUONMASS = 105.6583715 # MeV/c^2
ELECTRONMASS = 0.510998928
PIONMASS = 139.57018
PROTONMASS = 938.272046
KAONMASS = 493.677

class MuonTable(object):
  def __init__(self,fn="muE_liquid_argon.txt"):
    self.rho = 1.396 #g/cm^3
    self.Ts = []
    self.dEdxs = []
    self.ranges = []
    with open(fn) as infile:
      for line in infile:
        if line[0] == '#':
          continue
        T = line[10*0+1:10*0+11]
        dEdx = line[10*7+1:10*7+11]
        r = line[10*8+1:10*8+11]
        T = float(T)
        dEdx = float(dEdx)*self.rho
        r = float(r)/self.rho
        self.Ts.append(T)
        self.dEdxs.append(dEdx)
        self.ranges.append(r)

  def dEdx(self,ke):
    """
    Given a kinetic energy in MeV
    returns mean dEdx in MeV/cm
    """
    return numpy.interp(ke,self.Ts,self.dEdxs,left=float('nan'),right=float('nan'))

  def rangeCSDA(self,ke):
    """
    Given a kinetic energy in MeV
    returns CSDA range in cm
    """
    return numpy.interp(ke,self.Ts,self.ranges,left=float('nan'),right=float('nan'))

class Bethe(object):
    
  def __init__(self):
    """
    Setup everything for liquid argon
    """
    self.K = 0.307075 # MeV/mol cm^2
    self.Z = 18
    self.A = 39.948 #g/mol
    self.rho = 1.396 #g/cm^3
    self.z = 1
    self.hbarw = 22.85*1e-6 # MeV
    self.I = 188.0*1e-6 # MeV
    self.mec2 = 0.410999 #Mev/c^2
    self.j = 0.200
    self.a = 0.19559
    self.k = 3.
    self.x0 = 0.2000
    self.x1 = 3.0000
    self.Cbar = 5.2146
    self.delta0 = 0.
    if False: # silicon
      self.Z = 14
      self.A = 28.0855
      self.rho = 2.329
      self.hbarw = 31.05*1e-6 # MeV
      self.I = 173.0*1e-6 # MeV
      self.a = 0.14921
      self.k = 3.2546
      self.x0 = 0.2015
      self.x1 = 2.8716
      self.Cbar = 4.4355
      self.delta0 = 0.14

  def stoppingPower(self, l, momentum, Mparticle):
    """
    average -dE/dx in MeV cm^2 / g
    """
    energy, gamma, beta = self.getEnergyGammaBeta(momentum,Mparticle)
    Wmax = self.Wmax(beta,gamma,Mparticle)
    delta = self.delta(momentum,Mparticle)
    term1 = 0.5*math.log((2*self.mec2*beta**2*gamma**2*Wmax)/(self.I**2))
    term2 = - beta**2
    term3 = - 0.5 * delta
    result = term1 + term2 + term3
    result *= self.K*(self.z)**2 * self.Z / self.A / (beta**2) # now MeV cm^2 /g
    return result

  def mean(self, l, momentum, Mparticle):
    """
    average energy deposited in MeV for l in cm
    """
    result = self.stoppingPower(l,momentum, Mparticle) # in MeV cm^2 / g
    result *= self.rho # now in MeV/cm
    result *= l # now in MeV
    return result

  def mpv(self, l, momentum, Mparticle):
    """
    Most probable energy deposition in MeV
    """
    energy, gamma, beta = self.getEnergyGammaBeta(momentum,Mparticle)
    xi = self.xi(beta,l)
    delta = self.delta(momentum,Mparticle)
    term1 = math.log(2*self.mec2*beta**2*gamma**2/self.I)
    term2 = math.log(xi/self.I)
    result = term1 + term2 + self.j - beta**2 - delta
    result *= xi
    #result *= 1/(l*self.rho)# now in MeV cm^2 / g
    return result

  def width(self, l, momentum, Mparticle):
    """
    Landau width in MeV
    beta = v/c
    l in cm
    """
    energy, gamma, beta = self.getEnergyGammaBeta(momentum,Mparticle)
    return 4*self.xi(beta,l)

  def Wmax(self,beta,gamma,Mparticle):
    """
    Mparticle in MeV/c^2
    """
    num = 2*self.mec2*beta**2*gamma**2
    denom = 1 + 2*gamma*self.mec2/Mparticle + (self.mec2/Mparticle)**2
    result = num/denom
    return result

  def xi(self,beta,l):
    """
    beta = v/c
    l in cm
    Result in MeV
    """
    x = self.rho * l
    result = 0.5*self.K*self.Z/self.A*(self.z)**2*x/beta**2
    return result

  def delta(self,momentum,Mparticle):
    """
    delta(beta*Gamma)
    Argument is beta * gamma
    """
    x = math.log10(momentum/Mparticle)
    if x >= self.x1:
      return 2*math.log(10)*x - self.Cbar
    if x < self.x1 and x >= self.x0:
      return 2*math.log(10)*x - self.Cbar + self.a*(self.x1-x)**self.k
    if x < self.x0:
      return self.delta0*10**(2*(x-self.x0))
    raise Exception("Shouldn't have gotten past if statments")

  def getEnergyGammaBeta(self,momentum,mass):
    energy = math.sqrt(momentum**2+mass**2)
    gamma = energy / mass
    beta = momentum / energy
    return energy, gamma, beta

  def csdaRange(self,momentum,mass):
    r = 0.
    dl = 1.
    mom = momentum
    energy = math.sqrt(mom**2+mass**2)
    while True:
      mom = math.sqrt(energy**2-mass**2)
      dE = self.mean(dl,mom,mass)      
      energy -= abs(dE)
      r += dl
      if energy <= mass:
        break
    return r
