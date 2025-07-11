from kmk.keys import Key, make_argumented_key
from kmk.modules.holdtap import ActivationType, HoldTap, HoldTapKey


class TapDanceKey(Key):
    def __init__(self, *keys, tap_time=None, **kwargs):
        '''
        Any key in the tapdance sequence that is not already a holdtap
        key gets converted to a holdtap key with identical tap and hold
        attributes.
        '''
        super().__init__(**kwargs)
        self.tap_time = tap_time
        self.keys = []

        for key in keys:
            if not isinstance(key, HoldTapKey):
                ht_key = HoldTapKey(
                    tap=key,
                    hold=key,
                    prefer_hold=True,
                    tap_interrupted=False,
                    tap_time=self.tap_time,
                )
                self.keys.append(ht_key)
            else:
                self.keys.append(key)
        self.keys = tuple(self.keys)


class TapDance(HoldTap):
    def __init__(self):
        super().__init__(_make_key=False)
        make_argumented_key(
            names=('TD',),
            constructor=TapDanceKey,
            on_press=self.td_pressed,
            on_release=self.td_released,
        )

        self.td_counts = {}

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if isinstance(key, TapDanceKey):
            if key in self.td_counts:
                return key

        for _key, state in self.key_states.copy().items():
            if state.activated == ActivationType.RELEASED:
                keyboard.cancel_timeout(state.timeout_key)
                self.ht_activate_tap(_key, keyboard)
                self.send_key_buffer(keyboard)
                self.ht_deactivate_tap(_key, keyboard)
                keyboard.resume_process_key(self, key, is_pressed, int_coord)
                key = None

                del self.key_states[_key]
                del self.td_counts[state.tap_dance]

        if key:
            key = super().process_key(keyboard, key, is_pressed, int_coord)

        return key

    def td_pressed(self, key, keyboard, *args, **kwargs):
        # active tap dance
        if key in self.td_counts:
            count = self.td_counts[key]
            kc = key.keys[count]
            keyboard.cancel_timeout(self.key_states[kc].timeout_key)

            count += 1

            # Tap dance reached the end of the list: send last tap in sequence
            # and start from the beginning.
            if count >= len(key.keys):
                self.key_states[kc].activated = ActivationType.RELEASED
                self.on_tap_time_expired(kc, keyboard)
                count = 0
            else:
                del self.key_states[kc]

        # new tap dance
        else:
            count = 0

        current_key = key.keys[count]

        self.ht_pressed(current_key, keyboard, *args, **kwargs)
        self.td_counts[key] = count

        # Add the active tap dance to key_states; `on_tap_time_expired` needs
        # the back-reference.
        self.key_states[current_key].tap_dance = key

    d