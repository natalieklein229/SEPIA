% Testing prior sizes in matlab for various models
load('test_case_matlab.mat')
n_obs = 2;
n_sim = 5;
p = 3;
q = 4;
ell_sim = 80;
ell_obs = 20;
x = 0.5 * ones(n_sim, p);
y_ind = linspace(0, 100, ell_sim);
x_obs = 0.5 * ones(n_obs, p);
y_obs_ind = linspace(10, 85, ell_obs);

%% Set up struct array for observations
obs_noise_sd = 0.0001;
sigy = diag(ones(ell_obs,1) * obs_noise_sd.^2);
for i = 1:size(y_obs_std, 1)
   yobs(i).yStd = y_obs_std(i, :)';
   yobs(i).orig.t = y_obs_ind;
   yobs(i).Sigy = diag(ones(ell_obs,1));
end

%%  discrepancy for each
for i = 1:size(y_obs_std, 1)
    yobs(i).Dobs = ones(size(y_obs_ind, 2),1);
    yobs(i).x = x_obs(i, :);
    yobs(i).Kobs = Kobs';
end

%% Make structure for model
simData.x = [x, t]; % dummy x for first column
simData.yStd = y_sim_std';
simData.Ksim = Ksim';
simData.orig.y = y';
simData.orig.t = y_ind;
simData.orig.ysd = y_sd;

data.simData = simData;
data.obsData = yobs;

fprintf('ready to make gpmsa model\n')


%% Set up GPMSA
paramout = setupModel(data.obsData, data.simData);

%% prior sizes
