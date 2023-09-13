
def create_bucket(ingredients, today_full, today_y, user):
    string = "Список покупок для:" + user + "\n\nДата:" + today_full + "\n\n"
    string += '\n'.join([
            f' - {ingredient["ingredient__name"]}'
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients])
    string += '\n\nFoodgram (' + today_y + ')'

    return string
