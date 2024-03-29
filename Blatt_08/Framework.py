import numpy as np
import scipy.linalg 
  

def LUP(A):
    """Computes and returns an LU decomposition with pivoting. The return value  
       is a tuple (L,U,P) and fulfills L*U=P*A (* is matrix-multiplication)."""
   
    row, col = np.shape(A)
    U = np.copy(A)
    L = np.eye(row)
    P = np.eye(row)

    for k in range(row-1):
        i = k + np.argmax(abs(U[k:, k]))
        U[[k, i], k:] = U[[i, k], k:]
        L[[k, i], :k] = L[[i, k], :k]
        P[[k, i], :] = P[[i, k], :]

        for j in range(k+1, row):
            L[j, k] = U[j, k] / U[k, k]
            U[j, k] = U[j, k:] - (L[j, k] * U[k, k:])

    return L, U, P


def ForwardSubstitution(L,b):
    """Solves the linear system of equations L*x=b assuming that L is a left lower 
       triangular matrix. It returns x as column vector."""
   
    row, col = np.shape(L)
    x = np.zero((col, 1))
    
    for i in range(col):
        x[i, 0] = b[i, 0] / L[i, i]
        b[i+1:, 0] = b[i+1:, 0] - L[i+1:, i] * x[i, 0]

    return x

def BackSubstitution(U,b):
    """Solves the linear system of equations U*x=b assuming that U is a right upper 
       triangular matrix. It returns x as column vector."""
    
    row, col = np.shape(U)
    x = np.zeros((col, 1))

    for i in range(col-1, -1, -1):
        x[i, 0] = b[1, 0] / U[i, i]
        b[:i, 0] = b[:i, 0] - U[:i, i] * x[i, 0]

    return x
    
	
def SolveLinearSystemLUP(A,b):
    """Given a square array A and a matching vector b this function solves the 
       linear system of equations A*x=b using a pivoted LU decomposition and returns 
       x."""
   
    L, U, P = LUP(A)

    z = ForwardSubstitution(L,b)
    x = BackSubstitution(U,z)

    return x


def LeastSquares(A,b):
    """Given a matrix A and a vector b this function solves the least squares 
       problem of minimizing |A*x-b| and returns the optimal x."""
    

if(__name__=="__main__"):
    # A test matrix where LU fails but LUP works fine
    A=np.array([[1,2, 6],
                [4,8,-1],
                [2,3, 5]],dtype=np.double);
    b=np.array([[1],[2],[3]],dtype=np.double);
    # Test the LUP-decomposition
    L,U,P=LUP(A)
    print("L")
    print(L)
    print("U")
    print(U)
    print("P")
    print(P)
    print("Zero (LUP sanity check): "+str(np.linalg.norm(np.dot(L,U)-np.dot(P,A))))
    # Test the method for solving a system of linear equations
    print("Zero (SolveLinearSystemLUP sanity check): "+str(np.linalg.norm(np.dot(A,SolveLinearSystemLUP(A,b))-b)))
    # Test the method for solving linear least squares
    A=np.random.rand(6,4)
    b=np.random.rand(6)
    print("Zero (LeastSquares sanity check): "+str(np.linalg.norm(LeastSquares(A,b).flat-np.linalg.lstsq(A,b)[0])))
