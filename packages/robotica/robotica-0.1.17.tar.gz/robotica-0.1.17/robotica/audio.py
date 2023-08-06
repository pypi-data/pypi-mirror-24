""" Give verbal message. """
import asyncio
import logging
import shlex
from typing import Dict, List, Set

import yaml

logger = logging.getLogger(__name__)


class Audio:

    def __init__(self, loop: asyncio.AbstractEventLoop, config: str) -> None:
        self._loop = loop
        with open(config, "r") as file:
            self._config = yaml.safe_load(file)
        self._disabled = self._config['disabled']
        self._say_cmd = self._config.get('say_cmd') or []
        self._play_cmd = self._config.get('play_cmd') or []
        self._music_play_cmd = self._config.get('music_play_cmd') or []
        self._music_stop_cmd = self._config.get('music_stop_cmd') or []
        self._location = self._config.get('location')

    def is_action_required_for_locations(self, locations: Set[str]) -> bool:
        if self._disabled:
            return False
        return self._location in locations

    @staticmethod
    async def _execute(cmd_list: List[str], params: Dict[str, str]) -> None:
        for cmd in cmd_list:
            split = [
                value.format(**params) for value in shlex.split(cmd)
            ]
            logger.info("About to execute %s", split)
            process = await asyncio.create_subprocess_exec(*split)
            result = await process.wait()
            if result != 0:
                logger.info("Command %s returned %d", split, result)

    async def say(self, locations: Set[str], text: str) -> None:
        if self.is_action_required_for_locations(locations):
            logger.debug("About to say '%s'.", text)
            await self.music_stop(locations)
            await self.play(locations, 'prefix')
            await self._execute(self._say_cmd, {'text': text})
            await self.play(locations, 'repeat')
            await self._execute(self._say_cmd, {'text': text})
            await self.play(locations, 'postfix')
        else:
            logger.debug("Wrong location, not saying '%s'.", text)

    async def play(self, locations: Set[str], sound: str) -> None:
        sound_file = self._config['sounds'].get(sound)
        if not sound_file:
            return
        if self.is_action_required_for_locations(locations):
            logger.debug("About to play sound '%s'.", sound)
            await self._execute(self._play_cmd, {'file': sound_file})
        else:
            logger.debug("Wrong location, not playing sound '%s'.", sound)

    async def music_play(self, locations: Set[str], play_list: str) -> None:
        if self.is_action_required_for_locations(locations):
            logger.debug("About to play music '%s'.", play_list)
            await self._execute(self._music_play_cmd, {'play_list': play_list})
        else:
            logger.debug("Wrong location, not playing music '%s'.", play_list)

    async def music_stop(self, locations: Set[str]) -> None:
        if self.is_action_required_for_locations(locations):
            logger.debug("About to stop music.")
            await self._execute(self._music_stop_cmd, {})
        else:
            logger.debug("Wrong location, not stopping music.")
