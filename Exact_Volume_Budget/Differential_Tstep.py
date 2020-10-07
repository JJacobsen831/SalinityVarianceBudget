# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 11:10:28 2020

@author: Jasen
Tools used to create differential volumes and areas of each cell in roms output
takes time step into account

"""
import numpy as np
from netCDF4 import Dataset as nc4
import obs_depth_JJ as dep
import GridShft_3D as GridShift

def dV(tstep, RomsFile) :
    """ 
    Load roms grid at specific time step
    and computes differential volume of each cell
    """
    RomsNC = nc4(RomsFile, 'r')
   
    #compute depth at w points
    depth_domain = dep._set_depth(RomsFile, None, 'w',\
                                    RomsNC.variables['h'][:],\
                                    RomsNC.variables['zeta'][tstep, :, :, :])
        
    dz = np.diff(depth_domain, n = 1, axis = 0)
            
    #compute lengths of horizontal cell directions & repeat over depth space
    dx = np.repeat(1/np.array(RomsNC.variables['pm'][:]), \
                   dz.shape[0], axis = 0)
    dy = np.repeat(1/np.array(RomsNC.variables['pn'][:]), \
                   dz.shape[0], axis = 0)
    
    #compute differential volume of each cell
    DV = dx*dy*dz
    
    return DV
    
def dA(tstep, RomsFile, RomsGrd) :
    """
    Compute area of vertical grid cell faces 
    (Ax -> lat X depth, Ay -> lon X depth)
    """
    RomsNC = nc4(RomsFile, 'r')
    
    #depth at w points
    depth_w = dep._set_depth(RomsFile, None, 'w', RomsNC.variables['h'][:],\
                               RomsNC.variables['zeta'][tstep, :, :, :])
    dz_rho = np.diff(depth_w, n = 1, axis = 0)
    
    #average depth at w points to u points
    dz_u = GridShift.Rho_to_Upt(dz_rho)
    
    #average depth at w points to v points
    dz_v = GridShift.Rho_to_Vpt(dz_rho)
    
    #cell widths
    dx = np.repeat(1/np.array(RomsNC.variables['pm'][:]), dz_rho.shape[0])
    dy = np.repear(1/np.array(RomsNC.variables['pn'][:]), dz_rho.shape[0])
    
    #Area of face with x-normal
    Ax_norm = dz_u*dy
    
    #Area of face with y-normal
    Ay_norm = dz_v*dx
    
    return Ax_norm, Ay_norm

def dA_top(RomsNC):
    ndepth = RomsNC.variables['salt'][0, :, 0, 0].size
    
    #dlon dlat
    dx = 1/np.array(RomsNC.variables['pm'][:])
    dy = 1/np.array(RomsNC.variables['pn'][:])
    
    #dA
    dA = dx*dy
    dA_depth = np.repeat(np.array(dA)[np.newaxis, :, :], ndepth, axis = 0)
    
    return dA_depth 
    