import datetime

class MessageFormater():
    def _seconds_formatter(seconds):
        return str(datetime.timedelta(seconds=seconds))

    def _queue_line(index, data):
        return "{0}. : [{1}] - ({2})\n".format(index, data.title, MessageFormater._seconds_formatter(data.duration))

    @staticmethod
    def queue_message(queue, now_playing):
        formatter_start = "```markdown\n"
        now_playing = "# Now Playing: {0} - {1}\n".format(now_playing.title, MessageFormater._seconds_formatter(now_playing.duration))
        queue_message = "Song Queue: \n"
        for index, data in enumerate(queue):
            queue_message += MessageFormater._queue_line(index, data)
        formatter_end = "```"
        return formatter_start + now_playing + queue_message + formatter_end