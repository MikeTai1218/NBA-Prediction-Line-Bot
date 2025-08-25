from linebot.models import (
    TextSendMessage,
    ImageSendMessage,
    TemplateSendMessage,
    CarouselTemplate,
    MessageEvent,
)
from linebot.exceptions import LineBotApiError

from config import LINE_BOT_API
from utils.utils import *


def text_message(event: MessageEvent):
    message = event.message.text
    try:
        userUID = event.source.user_id
        profile = LINE_BOT_API.get_profile(userUID)
        userName = profile.display_name
    except LineBotApiError:
        LINE_BOT_API.reply_message(
            event.reply_token, TextSendMessage(text="Unknown User")
        )

    if message == "NBA每日預測":
        try:
            response, carouselColumns, gameOfTheDayPage, gameOfTheDayTime = (
                get_nba_game_prediction(playoffsLayout=False)
            )
            if not carouselColumns:
                LINE_BOT_API.reply_message(
                    event.reply_token, TextSendMessage(text=response)
                )

            carouselColumns += get_player_stat_prediction(
                gamePage=gameOfTheDayPage, gameTime=gameOfTheDayTime
            )
            respondMessages = [TextSendMessage(text=response)]
            for i in range(0, len(carouselColumns), 10):
                carouselTemplate = CarouselTemplate(columns=carouselColumns[i : i + 10])
                templateMessage = TemplateSendMessage(
                    alt_text="NBA每日預測", template=carouselTemplate
                )
                respondMessages.append(templateMessage)

            LINE_BOT_API.reply_message(event.reply_token, respondMessages)
        except Exception as err:
            LINE_BOT_API.reply_message(
                event.reply_token, TextSendMessage(text=str(err))
            )

    if message == "檢查":
        response = get_user_prediction_check(userName=userName)
        LINE_BOT_API.reply_message(event.reply_token, TextSendMessage(text=response))

    if message == "結算":
        try:
            response = settle_daily_prediction(playoffsLayout=False)
            LINE_BOT_API.reply_message(
                event.reply_token, TextSendMessage(text=response)
            )
        except Exception as err:
            errorMessage = TextSendMessage(text=str(err))
            respondMessage = TextSendMessage(
                text="?\n不是\n你們一個個天天都猴急什麼\n你們一急我又要上去查"
            )
            LINE_BOT_API.reply_message(
                event.reply_token, [errorMessage, respondMessage]
            )

    if message[:2] == "信仰":
        words = message.split()
        teamName = "" if len(words) != 2 else words[1]
        response = get_user_most_correct(
            userName=userName, teamName=teamName, correct=True
        )
        LINE_BOT_API.reply_message(event.reply_token, TextSendMessage(text=response))

    if message[:2] == "傻鳥":
        words = message.split()
        teamName = "" if len(words) != 2 else words[1]
        response = get_user_most_correct(
            userName=userName, teamName=teamName, correct=False
        )
        LINE_BOT_API.reply_message(event.reply_token, TextSendMessage(text=response))

    if message == "結算傻鳥":
        response = settle_most_correct_wrong()
        LINE_BOT_API.reply_message(event.reply_token, TextSendMessage(text=response))

    if message == "週排行":
        response = get_user_type_point("week_points")
        LINE_BOT_API.reply_message(event.reply_token, TextSendMessage(text=response))

    if message == "月排行":
        response = get_user_type_point("month_points")
        LINE_BOT_API.reply_message(event.reply_token, TextSendMessage(text=response))

    if message == "季排行":
        response = get_user_type_point("season_points")
        LINE_BOT_API.reply_message(event.reply_token, TextSendMessage(text=response))

    if message == "總排行":
        response = get_user_type_point("all_time_points")
        LINE_BOT_API.reply_message(event.reply_token, TextSendMessage(text=response))

    if message[:2] == "跟盤":
        words = message.split()
        userId = int(words[1]) if len(words) == 2 and words[1].isdigit() else -1
        response = get_prediction_by_id(userId=userId)
        LINE_BOT_API.reply_message(event.reply_token, TextSendMessage(text=response))

    if message[:2] == "比較":
        words = message.split()
        user1Id, user2Id = (
            (int(words[1]), int(words[2]))
            if len(words) == 3 and words[1].isdigit() and words[2].isdigit()
            else (-1, -1)
        )
        response = get_prediction_comparison(user1Id=user1Id, user2Id=user2Id)
        LINE_BOT_API.reply_message(event.reply_token, TextSendMessage(text=response))

    if message == "註冊":
        response = user_registration(userName=userName, userUID=userUID)
        LINE_BOT_API.reply_message(event.reply_token, TextSendMessage(text=response))

    if message == "NBA預測週最佳":
        bestMessage, rankMessage = get_user_type_best("week_points")
        if bestMessage:
            LINE_BOT_API.reply_message(
                event.reply_token,
                [TextSendMessage(text=bestMessage), TextSendMessage(text=rankMessage)],
            )
        else:
            LINE_BOT_API.reply_message(
                event.reply_token, TextSendMessage(text=rankMessage)
            )

    if message == "NBA預測月最佳":
        bestMessage, rankMessage = get_user_type_best("month_points")
        if bestMessage:
            LINE_BOT_API.reply_message(
                event.reply_token,
                [TextSendMessage(text=bestMessage), TextSendMessage(text=rankMessage)],
            )
        else:
            LINE_BOT_API.reply_message(
                event.reply_token, TextSendMessage(text=rankMessage)
            )

    if message == "NBA預測季最佳":
        bestMessage, rankMessage = get_user_type_best("season_points")
        if bestMessage:
            LINE_BOT_API.reply_message(
                event.reply_token,
                [TextSendMessage(text=bestMessage), TextSendMessage(text=rankMessage)],
            )
        else:
            LINE_BOT_API.reply_message(
                event.reply_token, TextSendMessage(text=rankMessage)
            )

    if message == "NBA猜一猜":
        try:
            usage, buttonsTemplate = get_nba_guessing()
            LINE_BOT_API.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=usage),
                    TemplateSendMessage(
                        alt_text="NBA猜一猜",
                        template=buttonsTemplate,
                    ),
                ],
            )
        except Exception as err:
            LINE_BOT_API.reply_message(
                event.reply_token, TextSendMessage(text=str(err))
            )

    if message.lower() == "news":
        response = get_hupu_news()
        LINE_BOT_API.reply_message(event.reply_token, TextSendMessage(text=response))

    if message[:2].lower() == "yt":
        response = get_youtube(keyword=message[3:])
        LINE_BOT_API.reply_message(event.reply_token, TextSendMessage(text=response))

    if message[:2].lower() == "gg":
        statusCode, imgSrc = get_google_image(message[3:])
        if statusCode == 200:
            LINE_BOT_API.reply_message(
                event.reply_token,
                ImageSendMessage(original_content_url=imgSrc, preview_image_url=imgSrc),
            )

    if message.lower() == "nba":
        pass
