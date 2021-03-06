
import scipy.io
import numpy as np

from sepia.SepiaModelSetup import setup_model
from sepia.SepiaData import SepiaData

matfile = scipy.io.loadmat('multi_sim_only_sepia_gpmsa_test.mat')

y = matfile['y'].T
y_ind = matfile['y_ind'].T
x = matfile['x']

data = SepiaData(x_sim=x[:, 0][:, None], t_sim=x[:, 1][:, None], y_sim=y, y_ind_sim=y_ind)
print(data)
data.standardize_y()
assert np.allclose(data.sim_data.y_std, matfile['ystd'].T, rtol=0.01)
data.transform_xt()
data.create_K_basis(n_pc=2)
assert np.allclose(data.sim_data.K, matfile['Ksim'].T, rtol=0.01)

model = setup_model(data)

ll = model.logLik()

print('sepia log lik: %0.5g, gpmsa log lik: %0.5g' % (ll, matfile['ll']))

if(0):
    nsamp = 100
    model.do_mcmc(nsamp)
    # Creates dict with each sampled variable name as key, array of samples (nsamp, ...) as value
    samples_dict = {p.name: np.array(p.mcmc.draws) for p in model.params.mcmcList}

    import matplotlib.pyplot as plt
    for i, k in enumerate(samples_dict.keys()):
        plt.subplot(1, 4, i+1)
        plt.hist(samples_dict[k].reshape(nsamp+1, -1))
        plt.title(k)
    plt.show()
