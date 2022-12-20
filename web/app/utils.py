def prepare_for_chartjs(data, label):

    colours = ['#007A78', '#002D85', '#003391', '#00389D', '#003EA9', '#0045B6', '#004BC2', '#0051CE', '#0058DA', '#005FE7', '#0167F3', '#0d6efd', '#1477FF', '#2680FF', '#3989FF', '#4C92FF', '#5E9CFF', '#71A7FF', '#84B1FF', '#97BCFF', '#AAC8FF', '#BDD3FF']

    dataset = {
        "labels": [str(x[0]) for x in data],
        "datasets": [{
            "label": label,
            "data": [x[1] for x in data],
            "backgroundColor": colours,
            "borderWidth": 1,
            "borderColor": colours,
        }]
    }
    return dataset