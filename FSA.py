import tempfile, subprocess
import pandas as pd

def fsa_wrapper(sdf, key, script='FSA.R'):
    tmpdir = tempfile.mkdtemp()
    fn = "%s/%s.csv" % (tmpdir, key) #absolute path
    sdf.to_csv(fn)
    subprocess.call(['/usr/bin/Rscript', script, '%s' % (fn)])
    
    return pd.read_table('%s.%s' % (fn, 'output'))