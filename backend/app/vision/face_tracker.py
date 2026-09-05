from dataclasses import dataclass, field

from app.vision.identity_voting import IdentityVoting


def overlap(a, b):
    top, right, bottom, left = a
    other_top, other_right, other_bottom, other_left = b
    intersection = max(0, min(right, other_right) - max(left, other_left)) * max(
        0, min(bottom, other_bottom) - max(top, other_top)
    )
    union = (right - left) * (bottom - top) + (other_right - other_left) * (
        other_bottom - other_top
    ) - intersection
    return intersection / union if union else 0


@dataclass
class Track:
    id: int
    box: tuple[int, int, int, int]
    seen: float
    stable_since: float
    last_recognition: float = 0
    voting: IdentityVoting = field(default_factory=IdentityVoting)

    @property
    def candidate(self):
        return self.voting.candidate

    @property
    def votes(self):
        return self.voting.votes

    def reset(self):
        self.voting.reset()

    def vote(self, candidate):
        return self.voting.observe(candidate)


class FaceTracker:
    def __init__(self):
        self.tracks: dict[int, Track] = {}
        self.next_id = 1

    def update(self, boxes, now):
        self.tracks = {key: value for key, value in self.tracks.items() if now - value.seen < 1.0}
        available = set(self.tracks)
        visible = []
        for box in boxes:
            best = max(available, key=lambda key: overlap(self.tracks[key].box, box), default=None)
            if best is None or overlap(self.tracks[best].box, box) < .45:
                track = Track(self.next_id, box, now, now)
                self.next_id += 1
                self.tracks[track.id] = track
            else:
                available.remove(best)
                track = self.tracks[best]
                if overlap(track.box, box) < .85:
                    track.stable_since = now
                    track.reset()
                track.box, track.seen = box, now
            visible.append(track)
        for key in available:
            self.tracks[key].reset()
            self.tracks[key].stable_since = now
        return visible
