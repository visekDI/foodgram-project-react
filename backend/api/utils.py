import io


def create_bucket(ingredients, today_full, today_y, user):
    string = 'Список покупок для:' + user + '\n\nДата:' + today_full + '\n\n'
    string += '\n'.join(
        [
            f' - {ingredient["ingredient__name"]}'
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        ]
    )
    string += '\n\nFoodgram (' + today_y + ')'

    return string


def create_shopping_list_buffer(ingredients, today_full, today_y, user):
    shoping_list = create_bucket(ingredients, today_full, today_y, user)
    shopping_list_buffer = io.BytesIO()
    shopping_list_buffer.write(shoping_list.encode("utf-8"))
    shopping_list_buffer.seek(0)
    return shopping_list_buffer
