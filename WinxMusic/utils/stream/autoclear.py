import os

from config import autoclean


async def auto_clean(popped):
    async def _auto_clean(popped_item):
        try:
            rem = popped_item["file"]
            autoclean.remove(rem)
            count = autoclean.count(rem)
            if count == 0:
                if "vid_" not in rem and "live_" not in rem and "index_" not in rem:
                    try:
                        os.remove(rem)
                    except:
                        pass
        except:
            pass

    if isinstance(popped, dict):
        await _auto_clean(popped)
    elif isinstance(popped, list):
        for pop in popped:
            await _auto_clean(pop)
    else:
        raise ValueError("Expected popped to be a dict or list.")
