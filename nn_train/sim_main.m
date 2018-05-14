%% Definition of parameters
% Geometric parameters
L = 50;
theta = deg2rad(30);
r = .5*L*sec(theta);
% Definition of origin points
po1 = [0, r, 0];
po2 = [r*cos(theta), -r*sin(theta), 0];
po3 = [-r*cos(theta), -r*sin(theta), 0];
% Focal length
F = 4.5; D = 14 * 25.4;
f = F * D;
% Overwrite f at 500 mm for prototype system
f = 500;
step = 0.0016;
%% Simulation
% Define sample size, feasible space and step parameters
N = 1000000;
h_max = 76.2;
h_min = 10;
h = h_max - h_min;
h_0 = .5*(h_max+h_min);
h_m = -h_0;
h_M = h_0;
step_size = 0.0016;
step_count = h/step_size;
% Seed RNG and establish random positions
rng(2017);
h1 = h_min + h.*rand(N, 1);
h2 = h_min + h.*rand(N, 1);
h3 = h_min + h.*rand(N, 1);
hs = [h1.*ones(N,1) h2.*ones(N,1) h3.*ones(N,1)];
% Create points from random heights
p1s = [zeros(N,1) r.*ones(N,1) h1.*ones(N,1)];
p2s = [r*cos(theta).*ones(N,1) -r*sin(theta).*ones(N,1) h2.*ones(N,1)];
p3s = [-r*cos(theta).*ones(N,1) -r*sin(theta).*ones(N,1) h3.*ones(N,1)];
% Set initial home points
po1s = [zeros(N,1) r.*ones(N,1) zeros(N,1)];
po2s = [r*cos(theta).*ones(N,1) -r*sin(theta).*ones(N,1) zeros(N,1)];
po3s = [-r*cos(theta).*ones(N,1) -r*sin(theta).*ones(N,1) zeros(N,1)];
% Calculate results of DK model
[dp, theta] = displacement(po1s, po2s, po3s, p1s, p2s, p3s, f);