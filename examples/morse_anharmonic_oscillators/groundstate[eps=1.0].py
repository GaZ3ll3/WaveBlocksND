dimension = 1
ncomponents = 1

potential = "morse_zero_2"
l = 1.0
x0 = 0.0

groundstate_of_level = 0

eps = 1.0

hawp_template = {
    "type" : "HagedornWavepacket",
    "dimension" : dimension,
    "ncomponents": 1,
    "eps" : eps,
    "basis_shapes" : [{
            "type" : "HyperbolicCutShape",
            "K" : 64,
            "dimension" : 1
            }]
    }

quadrature = {
    "type" : "HomogeneousQuadrature",
    'qr': {
        'type': 'TensorProductQR',
        'dimension': 1,
        'qr_rules': [{'dimension': 1, 'order': 68, 'type': 'GaussHermiteQR'}],
        }
    }
