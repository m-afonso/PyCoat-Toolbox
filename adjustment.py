from bath import Bath
from copy import copy


def adjust_bath(target_bath: Bath,
                initial_bath: Bath,
                resin: Bath,
                paste: Bath,
                water: Bath,
                target_weight: bool = True,
                paste_min: int | float = 0):

    bf = target_bath.weight
    p_bf = target_bath.pigment
    b_bf = target_bath.binder

    p_bi = initial_bath.pigment
    b_bi = initial_bath.binder

    b_r = resin.binder

    p_p = paste.pigment
    b_p = paste.binder

    w = 0
    while True:
        initial_bath_weight = (b_bf*bf*p_p - b_p*bf*p_bf + b_r*bf*p_bf - b_r*bf*p_p + b_r*p_p*w)/(b_bi*p_p - b_p*p_bi + b_r*p_bi - b_r*p_p)
        paste_weight = (-b_bf*bf*p_bi + b_bi*bf*p_bf - b_r*bf*p_bf + b_r*bf*p_bi - b_r*p_bi*w)/(b_bi*p_p - b_p*p_bi + b_r*p_bi - b_r*p_p)
        resin_weight = (b_bf*bf*p_bi - b_bf*bf*p_p - b_bi*bf*p_bf + b_bi*bf*p_p - b_bi*p_p*w + b_p*bf*p_bf - b_p*bf*p_bi + b_p*p_bi*w)/(b_bi*p_p - b_p*p_bi + b_r*p_bi - b_r*p_p)

        if paste_weight >= paste_min and initial_bath_weight >= 0 and paste_weight >= 0 and resin_weight >= 0:
            break

        if w > bf:
            break

        w += target_bath.weight / 1000

    initial_bath.weight = initial_bath_weight
    paste.weight = paste_weight
    resin.weight = resin_weight
    water.weight = w

    test_bath = copy(initial_bath)
    test_bath.add_bath(paste, resin, water)

    return {'target_bath': target_bath,
            'initial_bath': initial_bath,
            'resin': resin,
            'paste': paste,
            'water': water,
            'test_bath': test_bath}


if __name__ == '__main__':
    results = adjust_bath(Bath(5000, 0.25, 0.10),
                          Bath(0, 0.20, 0.09),
                          Bath(0, 0.36, .0),
                          Bath(0, 0.5, 10),
                          Bath(0, 0, 0))

    for result in results.keys():
        print(result, results[result])

