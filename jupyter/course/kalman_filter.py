# pylint: disable=invalid-name
import copy
from numpy.linalg import inv
import numpy as np

# Simple Kalman Filter Class that will be used to solve the Jovanovic and Muth problem
class KalmanFilter:
    """
    Kalman Filter class
    Takes:
        A: state transition matrix
        C: covariance matrix for the noise in the state transition
        G: observation matrix
        R: covariance matrix for the noise in the observation
        Σ: covariance matrix for the initial state vector (prior on variance)
        X: initial state vector mean
    Tracks:
        a: error for the state prediction
        K: Kalman gain parameter (regression coefficient)
        obs: observations
        Xs: state vector means
        Σ: covariance matrix for the state vector
        resids: residuals
        F: transition matrix for variance
        t: current time period
        num_states: number of states
    """

    def __init__(self, A, C, G, R, X, Σ):
        # We initialize the parameters of the Kalman Filter,ensuring they are valid numpy arrays
        self.A = np.atleast_2d(A)
        self.C = np.atleast_2d(C)
        self.G = np.atleast_2d(G)
        self.R = np.atleast_2d(R)
        self.Σ = np.atleast_2d(Σ)
        self.X = np.atleast_2d(X)
        self.Σ_prior = self.Σ
        self.X_prior = self.X
        self.a = np.atleast_2d(0)
        self.K = np.atleast_2d(1)
        self.y = np.atleast_2d(0)
        self.X_prime = np.atleast_2d(0)
        self.Σ_prime = np.atleast_2d(0)
        self.obs = []
        self.Xs = []
        self.Σs = []
        self.Ks = []
        self.resids = []
        self.Xs.append(self.X_prior)
        self.Σs.append(self.Σ_prior)
        self.F = self.A - self.K @ self.G
        # current time period
        self.t = 0
        # number of states
        self.num_states = len(self.X)

    def filter(self, y):
        """
        Given our observation y, we update the kalman gain and residuals
        """
        # Start with \hat{X}, \hat{\Sigma} from previous period (prior)
        self.y = np.atleast_2d(y)
        # Form prediction error on what we predict given prior vs. observed
        a = self.y - self.G @ self.X
        self.a = copy.deepcopy(a)
        self.obs.append(self.y)
        # We compute the Kalman gain parameter (regression coefficient)
        K = self.A @ self.Σ @ self.G.T @ inv(self.G @ self.Σ @ self.G.T + self.R)
        # Compute the residual of the observation compared to our prediction
        # Record the kalman gain and residuals
        self.Ks.append(K)
        self.K = copy.deepcopy(K)
        self.resids.append(a)

    def predict(self):
        """
        Given the new kalman gain and residuals, we update the state vector and covariance matrix
        """
        # Now we update our estimate of the state vector and covariance matrix using laws of motion
        self.X_prime = self.A @ self.X + self.K * self.a
        # Variance associated with $\nu$ noise
        F = self.A - self.K @ self.G
        # Ricatti equation for updating estimated variance of the state vector
        self.Σ_prime = (
            self.F @ self.Σ @ self.F.T + self.C @ self.C.T + self.K @ self.R @ self.K.T
        )
        # Update the state vector and covariance matrix as new priors
        self.t += 1
        self.F = copy.deepcopy(F)
        self.X = copy.deepcopy(self.X_prime)
        self.Σ = copy.deepcopy(self.Σ_prime)

    def record(self):
        """
        Records the state vector and the covariance matrix
        """
        self.Xs.append(self.X_prime)
        self.Σs.append(self.Σ_prime)

    def update(self, y):
        """
        Given the observation y, we update the state vector and covariance matrix and record them
        """
        self.y = np.atleast_2d(y)
        self.filter(self.y)
        self.predict()
        self.record()

    def forecast(self, h):
        """
        Forecast the state vector as a normal distributed variable for the next h periods
        """
        Xs = []
        Σs = []
        for _ in range(h):
            self.predict()
            Xs.append(self.X)
            Σs.append(self.Σ)
        return Xs, Σs

    def get_Xs(self):
        return self.Xs

    def get_Σs(self):
        return self.Σs

    def get_Ks(self):
        return self.Ks

    def get_resids(self):
        return self.resids

    def get_obs(self):
        return self.obs

    def reset(self):
        self.t = 0
        self.obs = []
        self.Xs = []
        self.Σs = []
        self.Ks = []
        self.obs = []
        self.resids = []
        self.Xs.append(self.X_prior)
        self.Σs.append(self.Σ_prior)
        self.K = np.atleast_2d(1)
