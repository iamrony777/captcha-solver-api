"""
Simple module to create a file after X seconds to trigger uvicorn reload
coz uvicorn's reload_delay param isn't working
"""
import asyncio
import os
import time


class Timeout:
    """Half-assed timeout class for uvicorn"""

    def __init__(self, filename: str, timeout: int = 10) -> None:
        self.filename = filename
        self.timeout = timeout # must be less than 60       
    def create_timeout_snippet(self) -> None:
        """just create a file"""
        with open('timeout', 'w', encoding='UTF-8') as timeout_file:
            timeout_file.write(f'{round(time.time())}')

    async def check_file(self) -> int:
        """Return Time passed since file's creation / modification, in seconds"""
        if os.path.exists(self.filename):
            creation_time = os.path.getctime(self.filename)
            utc_duration = time.gmtime(time.time() - creation_time)
            return utc_duration.tm_sec

    async def compare_time(self) -> bool:
        """checks and compares between file duration and timeout"""
        if (await self.check_file()) >= self.timeout:
            os.remove(self.filename) # here the captcha will be deleted
            self.create_timeout_snippet()
            return True
        return False

    async def run(self) -> None:
        """Start the loop"""
        while True:
            if not (await self.compare_time()):
                await asyncio.sleep(1)
            else:
                break



if __name__ == '__main__':
    tout = Timeout('test.log')
    asyncio.run(tout.run())

