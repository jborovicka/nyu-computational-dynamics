% Replication of the Mehra, Prescott (1985) economy

% parameters of the model
param.PHI = 0.43;    % persistence of each state
param.MU = 0.018;    % consumption growth rate mean
param.DELTA = 0.036; % growth rate dispersion

% transition matrix
param.P = [param.PHI   1-param.PHI;
           1-param.PHI param.PHI];
% consumption growth rate matrix
param.GAMMAC = [1+param.MU+param.DELTA 1+param.MU-param.DELTA;
                1+param.MU+param.DELTA 1+param.MU-param.DELTA];

% cash flow to be priced
param.GAMMAG = param.GAMMAC; % pricing the claim on aggregate consumption

% preference parameters and SDF
param.BETA =  0.98;
param.GAMMA = 5;
param.SDF = param.BETA * (param.GAMMAC).^(-param.GAMMA); % the .^ operator means elementwise power

% -------------------------------------------------------------------------
% solve model for a range of preference parameters
% original Mehra, Prescott (1985) region
beta_vec = linspace(0.001,1,100);
gamma_vec = linspace(0,10,200);
% extended region (uncomment if needed)
beta_vec = linspace(0.6,1.2,100);
gamma_vec = linspace(0,50,400);

ERe_mat = zeros(length(beta_vec),length(gamma_vec));
ERf_mat = zeros(length(beta_vec),length(gamma_vec));

for i = 1 : length(beta_vec)
    for j = 1 : length(gamma_vec)
        % preference parameters and SDF
        param.BETA =  beta_vec(i);
        param.GAMMA = gamma_vec(j);
        param.SDF = param.BETA * (param.GAMMAC).^(-param.GAMMA); % the .^ operator means elementwise power
        
        sol = evaluate_model(param);
        ERe_mat(i,j) = sol.ERe;
        ERf_mat(i,j) = sol.ERf;
    end
end

% -------------------------------------------------------------------------
%% display results
fprintf('Displaying results for parameter region beta = (%3.1f,%3.1f), gamma = (%3.1f,%3.1f).\n', ...
    beta_vec(1),beta_vec(end),gamma_vec(1),gamma_vec(end));
    
% risk premium and the risk-free rate
fig = figure;
scrs = get (0, 'ScreenSize');
set (fig, 'PaperPositionMode', 'auto');
set (fig, 'Position', [scrs(3)*1/4 scrs(4)*1/4 scrs(3)*1/2 scrs(4)*0.3]);

subplot(1,2,1);
contourf(gamma_vec,beta_vec,ERe_mat*100,[0.1 0.5 1 2 5 10 15],'ShowText','on');
title('Risk premium (%)');
xlabel('\gamma'); ylabel('\beta');
subplot(1,2,2);
contourf(gamma_vec,beta_vec,(ERf_mat-1)*100,[-50 -20 -5 0 2 5 10 20 50],'ShowText','on');
title('Risk-free rate (%)');
xlabel('\gamma'); ylabel('\beta');

% nonexistence regions
fig = figure;
scrs = get (0, 'ScreenSize');
set (fig, 'PaperPositionMode', 'auto');
set (fig, 'Position', [scrs(3)*3/8 scrs(4)*1/4 scrs(3)*1/4 scrs(4)*0.3]);

contourf(gamma_vec,beta_vec,isnan(ERe_mat),[1 1],'ShowText','on');
title('Dark region: Price-dividend ratio does not exist');
xlabel('\gamma'); ylabel('\beta');

% scatterplot
fig = figure;
scrs = get (0, 'ScreenSize');
set (fig, 'PaperPositionMode', 'auto');
set (fig, 'Position', [scrs(3)*3/8 scrs(4)*1/4 scrs(3)*1/4 scrs(4)*0.3]);

plot((ERf_mat(:)-1)*100,ERe_mat(:)*100,'*');
xlabel('Risk-free rate (%)'); ylabel('Risk premium (%)');
title(sprintf('Admissible region for \\beta\\in(%3.1f,%3.1f), \\gamma\\in(%3.1f,%3.1f)', ...
    beta_vec(1),beta_vec(end),gamma_vec(1),gamma_vec(end)));
xlim([-2 10]); ylim([0 15]);
% xlim([0 10]); ylim([0 2]);



%% ========================================================================
function sol = evaluate_model(param)

S = param.SDF;
P = param.P;
GAMMAG = param.GAMMAG;

N = size(S,1);
I = eye(N);

% first compute the unconditional stationary distribution PII
% (assuming it is unique)
% unconditional stationary distribution is the eigenvector of P' associated
% with eigenvalue equal to 1 (the largest eigenvalue)
[v,d] = eig(P');
[~,ind] = max(diag(d));
PII = v(:,ind) / sum(v(:,ind));

% conditional gross risk-free rate (Nx1 vector)
Rf = 1./ ((P.*S)*ones(N,1));
% unconditional gross risk-free rate
ERf = Rf'*PII;

% recursive formula for the price-dividend ratio: q =  P.*S.*G * (q + 1)
% solution given by
% q = inv(I - P.*S.*G) * (P.*S.*G)*1 = (I - P.*S.*G) \ (P.*S.*G)*1
% the .* operator is the elementwise multiplication, 1 is an Nx1 vector of ones

% solution for the infinite-horizon asset only valid
% if P.*S.*G has eigenvalues inside the unit circle
[~,d] = eig(P.*S.*GAMMAG);
maxeig = max(diag(d));

if (maxeig < 1)
    % asset price (Nx1 vector)
    q = (I - P.*S.*GAMMAG) \ ((P.*S.*GAMMAG)*ones(N,1));
    % returns (NxN matrix of returns R(i,j)
    R = (repmat(q',N,1) + 1) ./ repmat(q,1,N) .* GAMMAG;
    % conditional expected returns (Nx1 vector)
    EtR = diag(R * P');
    % unconditional expected return
    ER = EtR'*PII;
    % excess returns, realized and expected
    Re = R - repmat(Rf,1,N);
    EtRe = EtR - Rf;
    ERe = ER - ERf;
else
    q = nan(N,1);
    R = nan(N,N);
    EtR = nan(N,1);
    ER = nan;
    Re = nan(N,N);
    EtRe = nan(N,1);
    ERe = nan;
end

sol.PII = PII;
sol.Rf = Rf;
sol.ERf = ERf;
sol.q = q;
sol.R = R;
sol.EtR = EtR;
sol.ER = ER;
sol.Re = Re;
sol.EtRe = EtRe;
sol.ERe = ERe;

end