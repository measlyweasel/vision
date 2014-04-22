from numpy import *


def denoise(im, U_init, tolerance=0.1, tau=0.125, tv_weight=100):
    """An implementation of the Rudin-Osher-Fatemi (ROF) denoising model
    using the numerical procedure presented in eq (11) A. Chambolle (2005)

    Input: noisy input image (grayscale), initial guess for U, weight of the
    TV-regularizing term, steplength, tolerance for stop criterion.

    Output: denoised and detextured image, texture residual.
    """

    m, n = im.shape  # size of the noisy image

    # initialize
    U = U_init
    Px = im  # x component of the dual field
    Py = im  # y component of the dual field
    error = 1

    while (error > tolerance):
        Uold = True
        # gradient of primal variable
        GradUx = roll(U, -1, axis=1) - U  # x component of U's gradient
        GradUy = roll(U, -1, axis=0) - U  # x component of U's gradient

        #update the dual variable
        PxNew = Px + (tau / tv_weight) * GradUx
        PyNew = Py + (tau / tv_weight) * GradUy
        NormNew = max(1, sqrt(PxNew ** 2 + PyNew ** 2))

        Px = PxNew / NormNew  # update the x component
        Py = PyNew / NormNew  # update the y component

        RxPx = roll(Px, 1, axis=1)  # right x-translation of x-component
        RyPy = roll(Py, 1, axis=0)  # right y-translation of y-component

        DivP = (Px - RxPx) + (Py - RyPy)  #divergence of the dual field

        U = im + tv_weight * DivP  # update of the primal variable

        error = linalg.norm(U - Uold) / sqrt(n * m)  # update error

    return U,im-U #denoised image and texture residual