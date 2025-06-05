def calculate_cocomo(kloc, mode='organic'):
    mode_params = {
        'organic': (2.4, 1.05),
        'semidetached': (3.0, 1.12),
        'embedded': (3.6, 1.20)
    }
    if mode not in mode_params:
        raise ValueError('Invalid mode')

    a, b = mode_params[mode]
    effort = a * (kloc ** b)
    time = 2.5 * (effort ** 0.38)
    return {'effort': round(effort, 2), 'time': round(time, 2)}
