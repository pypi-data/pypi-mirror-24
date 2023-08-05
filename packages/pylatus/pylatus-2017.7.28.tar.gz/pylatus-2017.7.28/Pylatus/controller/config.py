#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore


class Config:
    QBA = QtCore.QByteArray()
    Settings = None
    DetAddress = '10.10.10.100:41234'
    Readout1 = '0.0023'
    Readout2 = '0.0130'
    Separator = '24'
    ServerDir = '/ramdisk/'
    LogFile = 'pylatus.log'
    UserDir = '/data/users/'
    DataDir = '/ramdisk/500_500'
    NoBeamCounts = '10'
    MonitorSpec = 'snbla1.esrf.fr:monitor:mon'
    MusstSpec = 'snbla1.esrf.fr:rhmusst'
    MusstTimeout1 = '0'
    MusstTimeout2 = '0'
    MusstFirmware = '/users/blissadm/local/isg/musst/pilatus_bm01.mprg'
    NumberOfFilters = '10'
    BeamstopOn = '0'
    BeamstopOff = '6'
    RootHash = 'e55761e10506cc773791f579b058c9d845e2a14a'
    Mono = 'mono'
    Phi = 'phi'
    Prphi = 'prphi'
    Omega = 'omega'
    Kappa = 'kappa'
    Bstop = 'bstop'
    Pldistf = 'pldistf'
    Pldistd = 'pldistd'
    Plvert = 'plvert'
    Plrot = 'plrot'
    Prver = 'prver'
    Prhor = 'prhor'
    Filter = 'filter'
    ScanAxis = 'mirror4'
    ScanTime = '0.1'
    ScanRange = '0.012'
    ScanStep = '0.001'
    ScanFilter = '7'
    MonitorMult = '1'
    Timescan = '0'
    MonoDspacing = '3.1356'  # Si 111
    MonoOffset = '0'
    MonSecName = 'sec'
    MonMeasTime = '0'
    MusstReadData = False
    AdjustThreshold = False
