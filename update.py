import os
from get_data import get_data
from generate_html import save_dashboard_html, save_municipality_maps


if __name__ == '__main__':
    get_data(archive=True)
    save_dashboard_html('static')
    save_municipality_maps(os.path.join('static', 'maps'))
