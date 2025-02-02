import numpy as np

class TRCA_Filter():

    def __init__(self, X_train, task_onsets, task_duration, sampling_rate=250) -> None:
        # For sanity:
        # X_train -> N, T
        # task_onsets -> Vector of task onsets
        # task_duration -> Given in seconds

        N = X_train.shape[0]
        num_blocks = len(task_onsets)
        block_len = int(task_duration * sampling_rate)

        S = np.zeros((N,N))

        for i in range(N):
            for j in range(N):
                for k in range(num_blocks):
                    for l in range(num_blocks):
                        if k != l:
                            tk = task_onsets[k]
                            tl = task_onsets[l]
                            xi = X_train[i, tk :tk + block_len]
                            xj = X_train[j, tl : tl + block_len]
                            xi_centered = xi - np.mean(xi)
                            xj_centered = xj - np.mean(xj)
                            S[i, j] += np.dot(xi_centered, xj_centered)

        # Sum over col axis, keep dim to maintain dimension
        mean_X = np.mean(X_train, axis=1, keepdims=True)
        X_cleaned = X_train - mean_X
        Q = X_cleaned @ X_cleaned.T

        V, D = np.linalg.eig(np.linalg.pinv(S) @ Q)

        self.filter_matrix = np.transpose(V)

    def __call__(self, X):
        # X -> Matrix to predict (N (num channels), T (time points))
        return self.filter_matrix @ X

