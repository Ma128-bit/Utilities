import sys, os, subprocess, uproot, joblib
import numpy as np
import pandas as pd
from ROOT import RDF
from sklearn.ensemble import HistGradientBoostingClassifier
"""
branches_MVA =[
    "Ptmu", "Etamu", "Vx", "Vy", "Vz", "cQ_uS_", "cQ_tK_", "cQ_gK_", "cQ_tRChi2_",
    "cQ_sRChi2_", "cQ_Chi2LP_", "cQ_Chi2LM_", "cQ_lD_", "cQ_gDEP_", "cQ_tM_", "cQ_gTP_", 
    "match1_dX_", "match1_pullX_", "match1_pullDxDz_", "match1_dY_", "match1_pullY_", "match1_pullDyDz_", 
    "match2_dX_", "match2_pullX_", "match2_pullDxDz_", "match2_dY_", "match2_pullY_", "match2_pullDyDz_", 
    "validMuonHitComb", "nValidTrackerHits",
    "nValidPixelHits", "GL_nValidMuHits", "nStMu", "nMatchesMu", 
    "innerTrk_ValidFraction_", "innerTrk_highPurity_", 
    "innerTrk_normChi2_", "outerTrk_normChi2_", "outerTrk_muStValidHits_"   
]
"""
branches_MVA = [
    'cQ_Chi2LP_',
    'cQ_tK_',
    'nValidTrackerHits',
    'nValidPixelHits',
    'innerTrk_ValidFraction_',
    'cQ_Chi2LM_',
    'cQ_sRChi2_',
    'cQ_tRChi2_',
    'cQ_gDEP_',
    'cQ_gK_',
    'trkLayersWMeas',
    'nStMu',
    'segmComp_',
    'GLnormChi2_mu',
    'innerTrk_normChi2_',
    'outerTrk_normChi2_'
]
def load_data(file_name):
    """Load ROOT data and turn tree into a pd dataframe"""
    print("Loading data from", file_name)
    f = uproot.open(file_name)
    tree = f["FinalTree"]
    data = tree.arrays(library="pd")
    return data

def save_data(data, fileName):
    data.to_csv(fileName+".csv", index=False)
    print("File CSV saved!")
    del data
    rdf = RDF.FromCSV(fileName+".csv")
    rdf.Snapshot("FinalTree", fileName+".root")
    print("File ROOT saved!")

def predict(data, index, model):
    branches = [var + str(index) for var in branches_MVA]
    X = data[branches]
    X = X.rename_axis(None, axis=1)
    predictionsID = model.predict(X)
    predictions = model.predict_proba(X)
    data["privateMVAID_mu"+str(index)] = predictionsID
    data["privateMVA_mu"+str(index)] = predictions[:,1]
    del predictions
    del predictionsID
    del X
    return data


if __name__ == "__main__":
    file = "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/JobAdd_perEra/Era_C_tau3mu.root"
    #file = "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/JobAdd_perEra/MC_Ds_preE.root"
    #file = "/lustrehome/mbuonsante/Tau_3mu/Ntuple/CMSSW_13_0_13/src/Analysis/JobAdd_perEra/MC_Bp_preE.root"
    model = joblib.load('privateMVA.pkl')
    data = load_data(file)
    print(len(data))
    """
    branches_temp = [var + str(1) for var in branches_MVA] + [var + str(2) for var in branches_MVA] + [var + str(3) for var in branches_MVA]
    for v in branches_temp:
        print(v, " : ", (data[v] == -99).sum())
    
    print(len(data))
    data = data[(data[branches_temp] != -99).all(axis=1)]
    """
    for i in range(1,4):
        print(i)
        predict(data, i, model)
    save_data(data, "test")

