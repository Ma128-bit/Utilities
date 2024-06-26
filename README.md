# Utilities
Plots for CC and other things done between ntuple/analysis and xgboost

## Setting the environment

```
cmsrel CMSSW_13_0_13
cd CMSSW_13_0_13/src
cmsenv
git clone https://github.com/Ma128-bit/CC_etc/ .
scram b -j20
```

## Description of scripts
* `SelEffNtuple.py` or `SelEffAna.py`
  * Run as: `python3 SelEffNtuple.py` or `python3 SelEffAna.py`
  * Default: MC - Control channel. Pass `--tau3mu` and/or `--data`
  * Out: .csv file with number of events per era and per cut
  * Description: It is used to obtain the selection efficiencies starting from data after Ntuplizer/Analysis
* `Small_SelEffNtuple.py`
  * Run as: `python3 Small_SelEffNtuple`
  * Is a smaller version or SelEffNtuple.py, it runs on a subsample of data (only tau3mu)

* `Control.py`
  * Run as: `python3 Control.py --year 2022`
  * Options: `--year` : `2022` or `2023` and `--plots` for control plots
  * Out: Control_Plots and Mass_Fits directories with Control plots and invariant mass fits

* `PV_mkIsto.py`
  * Run as: `python3 PV_mkIsto.py`
  * Out: PV_Histo directory with nVTx histograms for data and MC and their ratio
 
* `New_Ntuple.py` or `New_Ntuple_small.py`
  * Run as: `python3 New_Ntuple.py --type X`
    * with `X` = `tau3mu2022`/`tau3mu2023` or `control2022`/`control2023`
  * Out: ROOTFiles directory with merged analysis files and weights used as input to XGBoost 
