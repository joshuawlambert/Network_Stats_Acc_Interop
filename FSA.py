import tempfile, subprocess

def fsa_wrapper(sdf, key):
    tmpdir = tempfile.mkdtemp()
    fn = "%s/%s.csv" % (tmpdir, key) #absolute path
    sdf.to_csv(fn)
    subprocess.call(['/usr/bin/RScript', 'FSA.R', '%s' % (fn)])
    
    return pd.read_table('%s.%s' % (fn, 'output'))