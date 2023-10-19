# -*- coding: utf-8 -*-

class HandlingException(Exception):
    def __init__(self, status: int):
        super().__init__()
        self.status = status
