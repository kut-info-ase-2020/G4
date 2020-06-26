
# https://ja.wikipedia.org/wiki/%E4%B8%8D%E5%BF%AB%E6%8C%87%E6%95%B0#:~:text=%E4%B8%8D%E5%BF%AB%E6%8C%87%E6%95%B0%EF%BC%88%E3%81%B5%E3%81%8B%E3%81%84%E3%81%97%E3%81%99%E3%81%86,%E6%B8%A9%E7%86%B1%E6%8C%87%E6%A8%99%E3%81%AE%E4%B8%80%E3%81%A4%E3%80%82
def compute_discomfort_index(temp, humid):
    discomfort_index = 0.81 * temp + 0.01 * humid * (0.99 * temp - 14.3) + 46.3
    return discomfort_index
