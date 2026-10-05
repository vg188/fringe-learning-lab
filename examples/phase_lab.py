"""Standard-library numerical checks for the fringe-projection tutorial.
Educational simulations only. No trained neural network or hardware is used.
Run: python examples/phase_lab.py
"""
import csv,json,math,random,statistics
from pathlib import Path
TAU=2*math.pi
OUT=Path(__file__).resolve().parent

def wrap(x):
    return (x+math.pi)%TAU-math.pi

def sample(n,a,b,phase,noise=0,rng=None):
    if not isinstance(n,int) or n<3: raise ValueError('N must be an integer >= 3')
    rng=rng or random.Random(0)
    return [a+b*math.cos(phase-TAU*i/n)+rng.gauss(0,noise) for i in range(n)]

def extract(values,threshold=1e-10):
    n=len(values)
    if n<3 or not all(math.isfinite(v) for v in values): raise ValueError('Need >=3 finite samples')
    m=sum(v*math.sin(TAU*i/n) for i,v in enumerate(values))
    d=sum(v*math.cos(TAU*i/n) for i,v in enumerate(values))
    b=2*math.hypot(m,d)/n
    return {'A':sum(values)/n,'B':b,'phase':None if b<threshold else wrap(math.atan2(m,d)),'M':m,'D':d}

def unwrap_temporal(wrapped_high,absolute_low,ratio):
    k=round((ratio*absolute_low-wrapped_high)/TAU)
    return wrapped_high+TAU*k,k

def main():
    reference=extract(sample(4,100,40,math.pi/6))
    assert abs(reference['A']-100)<1e-10
    assert abs(reference['B']-40)<1e-10
    assert abs(wrap(reference['phase']-math.pi/6))<1e-10
    maxerr=0
    for n in (3,4,12):
        for angle in (-179,-120,-90,-30,0,30,90,120,179):
            p=math.radians(angle); est=extract(sample(n,100,40,p))
            maxerr=max(maxerr,abs(wrap(est['phase']-p)))
    assert maxerr<1e-10
    invalid=extract([100,100,100,100]);assert invalid['phase'] is None
    high,k=unwrap_temporal(-.8*math.pi,.8*math.pi,4)
    assert k==2 and abs(high-3.2*math.pi)<1e-10
    rng=random.Random(20261005); trials=10000; amplitude=40;noise=2;stats=[];rows=[]
    for n in (3,4,12):
        errors=[]
        for j in range(trials):
            p=rng.uniform(-math.pi,math.pi)
            estimate=extract(sample(n,100,amplitude,p,noise,rng))
            error=wrap(estimate['phase']-p);errors.append(error)
            rows.append((n,j,p,estimate['phase'],error))
        rmse=math.sqrt(statistics.mean(e*e for e in errors))
        theory=math.sqrt(2*noise**2/(n*amplitude**2))
        assert abs(rmse/theory-1)<.08
        stats.append({'N':n,'trials':trials,'RMSE_rad':rmse,'small_noise_theory_rad':theory})
    results={'purpose':'Educational simulation, not paper reproduction','phase_convention':'I_n=A+B*cos(phi-2*pi*n/N)','seed':20261005,'noise_sigma_per_frame':noise,'amplitude':amplitude,'four_step_example':reference,'all_quadrants_max_error_rad':maxerr,'zero_modulation_phase':None,'temporal_example':{'k':k,'phase_rad':high},'noise_trials':stats}
    (OUT/'results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False,allow_nan=False),encoding='utf-8')
    with (OUT/'noise_trials.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f);writer.writerow(['N','trial','true_phase_rad','estimated_phase_rad','circular_error_rad']);writer.writerows(rows)
    print('PASS: exact recovery for 3/4/12 steps and all tested quadrants')
    print('PASS: zero modulation marked invalid; temporal fringe order = 2')
    print('Four-step example: A=%.6f B=%.6f phase=%.6f degrees'%(reference['A'],reference['B'],math.degrees(reference['phase'])))
    for s in stats:print('N=%2d RMSE=%.6f rad; small-noise theory=%.6f rad'%(s['N'],s['RMSE_rad'],s['small_noise_theory_rad']))
    print('Saved:',OUT/'results.json',OUT/'noise_trials.csv')

if __name__=='__main__':main()
