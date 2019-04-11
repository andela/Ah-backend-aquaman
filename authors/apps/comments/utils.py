from rest_framework import response, status


class CommentsUtilities:

    @staticmethod
    def check_for_highlited_range(request, article, data):
        if "first_highlited" in request and "last_highlited":
            if isinstance(request["first_highlited"], int) and \
                    isinstance(request['last_highlited'], int):

                return CommentsUtilities.check_for_response(request, article, data)
            return response.Response(
                {
                    "error": "first_highlited and last_highlited fields should be intergers."
                },
                status.HTTP_400_BAD_REQUEST
            )
        return data

    @staticmethod
    def check_values_greater_text(request, article):
        if (request["first_highlited"] < len(article)) \
            and (request["last_highlited"] < len(article)):
            return True
        return response.Response(
            {
                "error": "first_highlited or last_highlited is out of index."
            },
            status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def check_first_greater_last(request):
        if request['first_highlited'] < request['last_highlited']:
            return True
        return response.Response(
            {
                "error": "first_highlited should be less than last_highlited."
            },
            status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def check_for_response(request, article, data):
        all_checks = [
            CommentsUtilities.check_first_greater_last(request),
            CommentsUtilities.check_values_greater_text(request, article)
        ]
        for check in all_checks:
            if isinstance(check, response.Response):
                return check
        data["highlighted_text"] = article[request["first_highlited"]:request["last_highlited"]]
        return data
