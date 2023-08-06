Quantum Spin
----------------

This is a little package that will help with learning how quantum spin and entanglement work.
It is meant to complement some of the "theoretical minimum" lectures and other web resources.

- [https://en.wikipedia.org/wiki/Pauli_matrices]
- [https://en.wikipedia.org/wiki/Triplet_state]
- [https://en.wikipedia.org/wiki/Von_Neumann_entropy]
- Book: **Quantum Mechanics - The Theoretical Minimum**, Leanoard Susskind and Art Friedman, Basic Books, 2014. (mostly chapters 6&7)
- [http://theoreticalminimum.com/courses/quantum-mechanics/2012/winter/lecture-6] and 7

Eventually I hope to work this in to understanding more about quantum computing.

Examples of code use.
-------------------------

**Out-of-the box tests**:
    
.. code:: python

    import qspin
    qspin.test_spin()
    qspin.test_entangled()

**Spin states**, up, down and linear combinations to form mixed states

.. code:: python

    >>> from qspin import bra,ket,u,d,s0,sx,sy,sz
    >>> u
    1.0 |u> 
    >>> d
    1.0 |d> 
    >>> u + d
    1.0 |u>  + 1.0 |d> 
    >>> u + i*d
    (1+0j) |u>  + 1j |d> 

**Operators**

.. code:: python

    >>> sx # Pauli spin matrix
    [[0 1]
     [1 0]]
    >>> sy
    [[ 0.+0.j -0.-1.j]
     [ 0.+1.j  0.+0.j]]
    >>> sz
    [[ 1  0]
     [ 0 -1]]
    >>> sz*u
    1.0 |u>
    >>> sz*d
    -1.0 |d>

Expected value (.H is Hermetian conjugate; it converts a ket to a bra).
sz is the observable for z-component of spin, For the "up" state, the only
outcome us +1, so the expected value is +1.

.. code:: python

    >> u.H*sz*u
    1.0

The operator (sz in this case) is known in quantum mechanics as an "observable,"
meaning it measures something. Here it is the z-component of spin.
The eigenvalues of the observable are the possible outcomes the observation.
Underlying each state is a wave function. We store the wave function internally
as vector, with each component being the wave function value for the basis eigenstate.
The operators (observables) are stored as matrices, also defined on the same basis.
The assumed basis throughout qspin is '|u>' and '|d>' for single particles.

.. code:: python

    >>> u
    1.0 |u> 
    >>> u.phi
    matrix([[ 1.],
            [ 0.]])

We can evaluate the eigenvales and eigenvectors of observables. ".op" pulls out the matrix.

.. code:: python

    >>> import numpy as np
    >>> sz
    [[ 1  0]
     [ 0 -1]]
    >>> ev, evec = np.linalg.eig(sz.op)
    >>> ev
    array([ 1., -1.])
    >>> evec
    matrix([[ 1.,  0.],
            [ 0.,  1.]])
    >>> sx # spin x
    [[0 1]
     [1 0]]
    >>> ev, evec = np.linalg.eig(sx.op)
    >>> ev
    array([ 1., -1.])
    >>> evec
    matrix([[ 0.70710678, -0.70710678],
            [ 0.70710678,  0.70710678]])

Note that the spin-x observerable has the same eigenvalues as spin-z, +1 and -1. But the eigenvectors
are different, in our basis, since we are using the {|u>, |d>} basis. They are
:math:`(|u> + |d>)/\sqrt{2}`, which measures as sx = +1, and
:math:`(|u> - |d>)/\sqrt{2}`, which measures as sx = -1.

Conditional probabilities are calculated using inner products of states with the
eigenvectors of the measurment, squared. So the probability
of measuring sx = +1 given and electron prepared in state |u> is:

.. code:: python

    >>> l = (u+d).normalized # "left" - the eigenvector for sx = +1 (+1 eigenvalue of sx)
    >>> (bra(l)*ket(u))**2   # or ( l.H * u )**2 since .H converts to bra
    0.5

We can use strings to generate the basis states for electrons and electron pairs.

.. code:: python

    >>> u = ket('|u>')
    >>> d = ket('|d>')
    >>> u
    1.0 |u>
    >>> d
    1.0 |d>

States can also be defined using the wave function, given
in the form of a matrix column vector. And it is good practice
to normalize states.

.. code:: python

    >>> w = ket( np.matrix([1.,1.]).T).normalized()
    >>> w
    0.707106781187 |u>  + 0.707106781187 |d> 
    
In the *future*, we might allow defining arbitrary states as strings, as in:
*(caution, none of this works yet)*

.. code:: python

    >>> l = ket( (u + d).normalized(), '|l>')
    >>> r = ket( (u - d).normalized(), '|r>')
    >>> ket('|r>')
    0.707106781187 |u>  - 0.707106781187 |d> 
    >>> l + r
    1.0 |u>
    >>> lr_basis = ['|l>','|r>']  # and maybe even allow converting to this basis
    >>> l + r | lr_basis
    0.707106781187 |l>  - 0.707106781187 |r>

(now back to working code again)

Form a projection operator from outer products of basis states.

.. code:: python

    >> rho = ket('|u>') * bra('<u|') + ket('|d>') * bra('<d|')
    >> # can also do this:
    >> u = ket('|u>'); d = ket('|d>');
    >> rho = ket(u) * bra(u) + ket(d) * bra(d)
    >>> rho
    [[ 1.  0.]
     [ 0.  1.]]
    >>> u
    1.0 |u> 
    >>> rho*u
    1.0 |u> 
    >>> rho*d
    1.0 |d> 

Note that bra(ket(...)) and ket(bra(...)) convert, and takes care of the complex-conjugating.

.. code:: python

    >> u.kind
    'ket'
    >> bra(u).kind
    'bra'


Here we create a **density matrix** for an ensemble of single particles.

.. code:: python

    >> from qspin import entropy
    >> P = [0.5, 0.5]
    >> rho = P[0] * bra('|u>').density() + P[1] * bra('|d>').density() # make sure the probabilities add to one
    >> entropy(rho) # it's not zero because there is a mixture of states
    0.69314718055994529
    >> rho = ( bra('|u>') + bra('|d>') ).normalized().density()
    >> entropy(rho) # this one is zero because all electrons are prepared in the "u+d" state
    0
    
Make sure you normalize any states you define, using the call to .normalized(). [Maybe I should check for this in future versions]

**Quantum state of two electrons**

The basis states of electron pairs
can be built up from basis states of the single electrons, via tensor product.
** is the tensor product.
(Note there are already ready-made u,d,uu,ud,du,dd states in qspin).

.. code:: python

    >>> uu = ket('|u>') ** ket('|u>')  # or: u = ket('|u>'); uu = u**u
    >>> ud = ket('|u>') ** ket('|d>')
    >>> du = ket('|d>') ** ket('|u>')
    >>> dd = ket('|d>') ** ket('|d>')
    >>> ud = ket('|ud>'); du = ket('|du>') # also works
    >>> sing = (ket('|ud>') - ket('|du>')).normalized() # singlet state of entangled pair
    >>> sing
    0.707106781187 |ud>  - 0.707106781187 |du> 

Same with two-particle operators - tensor products of single particle operators.
s0 is the identity operator.

.. code:: python

    >>> sigx = s0**sx
    >>> taux = sx**s0

**Entangled pairs**

Once you have created a (possibly) entangled pair state, you can test it for entanglement:

.. code:: python

    >>> sing = (ket('|ud>') - ket('|du>')).normalized()
    >>> sing.entangled()
    True
    >>> sing.entropy()
    1.3862943611198908
    >>> sing.correlation()
    -0.9999999999999998
    >>> uu.entangled()
    False

I'd like to extend the codes to allow three and more particle states, with tests for entanglement
and examples of the entanglement monogamy theorem.