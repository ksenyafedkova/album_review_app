import logging

logging.basicConfig(
    filename='garbage/app.log',
# /Users/ksenia/PycharmProjects/album_review_app/garbage
# /Users/ksenia/PycharmProjects/garbage/app.log'
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)