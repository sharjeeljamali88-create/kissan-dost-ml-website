"""Reproducible small-data forecast. Run: python train.py"""
import csv, json, math
from pathlib import Path
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
ROOT=Path(__file__).resolve().parent
SOURCE='https://finance.gov.pk/survey/chapter_25/2_Agriculture.pdf'
def train():
 rows=list(csv.DictReader((ROOT/'data/pakistan_yield_history.csv').open()))
 bundle={'source':SOURCE,'table':'Table 2.5, Pakistan Economic Survey 2024–25','scope':'Pakistan national averages; not district or farm predictions','vintage':'2024–25 report; final year provisional','crops':{}}
 for crop in ['Wheat','Cotton','Sugarcane']:
  series=sorted([r for r in rows if r['crop']==crop],key=lambda r:int(r['year']))
  years=np.array([int(r['year']) for r in series]); y=np.array([float(r['yield_kg_ha']) for r in series])
  X=np.column_stack([years[1:]-2010,y[:-1]]); target=y[1:]
  def estimator():return make_pipeline(StandardScaler(),Ridge(alpha=10.0))
  tests=[]
  for i in range(len(target)-5,len(target)):
   m=estimator().fit(X[:i],target[:i]);pred=float(m.predict(X[i:i+1])[0])
   tests.append({'year':int(years[i+1]),'actual':float(target[i]),'predicted':pred,'baseline':float(y[i])})
  m=estimator().fit(X,target);sc=m[0];reg=m[1]
  errors=np.array([t['actual']-t['predicted'] for t in tests]);base=np.array([t['actual']-t['baseline'] for t in tests])
  pred=float(m.predict([[2026-2010,y[-1]]])[0]);mae=float(np.abs(errors).mean()); baseline_mae=float(np.abs(base).mean())
  bundle['crops'][crop]={'mean':sc.mean_.tolist(),'scale':sc.scale_.tolist(),'coef':reg.coef_.tolist(),'intercept':float(reg.intercept_),'forecast_year':2026,'forecast_kg_ha':pred,'last_yield':float(y[-1]),'mae_kg_ha':mae,'rmse_kg_ha':float(np.sqrt((errors**2).mean())),'baseline_mae_kg_ha':baseline_mae,'backtest':tests,'history':[{'year':int(a),'yield':float(b)} for a,b in zip(years,y)],'training_samples':len(target),'basis':'cotton lint' if crop=='Cotton' else 'harvested crop','beats_baseline':mae<baseline_mae}
 (ROOT/'dist/model.json').write_text(json.dumps(bundle,indent=2))
 (ROOT/'backend/model.json').write_text(json.dumps(bundle,indent=2))
 print(json.dumps({k:{x:v[x] for x in ['forecast_kg_ha','mae_kg_ha','baseline_mae_kg_ha','beats_baseline']} for k,v in bundle['crops'].items()},indent=2))
if __name__=='__main__':train()
