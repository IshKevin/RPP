from __future__ import annotations

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

Language = Literal["en", "fr"]
Channel = Literal[
    "Amazon",
    "Audible",
    "TikTok",
    "YouTube",
    "Instagram",
    "Facebook",
    "LinkedIn",
    "X",
    "Email",
    "WhatsApp",
    "Website",
    "Podcast",
]


class BookInput(BaseModel):
    title: str = Field(..., min_length=1)
    subtitle: Optional[str] = None
    description: str = Field(..., min_length=10)
    author_name: str = Field(..., min_length=2)
    language: Optional[Language] = None
    categories: List[str] = Field(default_factory=list)
    url: Optional[str] = None


class Persona(BaseModel):
    name: str
    pains: List[str] = Field(default_factory=list)
    desires: List[str] = Field(default_factory=list)
    triggers: List[str] = Field(default_factory=list)


class ChannelMessage(BaseModel):
    channel: Channel
    hook: str
    body: str
    cta: str


class VideoAd(BaseModel):
    angle: str
    script: str
    overlay_text: List[str] = Field(default_factory=list)
    footage_keywords: List[str] = Field(default_factory=list)
    music_keywords: List[str] = Field(default_factory=list)


class LaunchPack(BaseModel):
    language: Language
    personas: List[Persona]
    channel_messages: List[ChannelMessage]
    emotional_angles: List[str]
    gift_ideas: List[str]
    keywords: List[str]
    hashtags: List[str]
    video_ads: List[VideoAd]


class HealthResponse(BaseModel):
    status: str
    version: str
EOF