import ctypes
import numpy as np
from picosdk.ps2000a import ps2000a as ps
from picosdk.functions import adc2mV, assert_pico_ok


class PicoAWG:
    def __init__(self, chandle):
        self.chandle = chandle
        self.offset = 0
        self.pk_to_pk = 2 * 10**6
        self.wave_type = None
        self.start_frequency = None
        self.stop_frequency = None
        self.increment = 0
        self.delta_phase_increment = 0
        self.dwell_time = 1
        self.dwell_count = 0
        self.sweep_type = 0
        self.operation = 0
        self.shots = 0
        self.sweeps = 0
        self.triggertype = 0
        self.triggerSource = 0
        self.extInThreshold = 1
        self.index_mode = 0
        self.waveform_data = None

    def set_sig_gen_built_in(
        self,
        offset,
        pk_to_pk,
        wave_type,
        start_frequency,
        stop_frequency,
        increment,
        dwell_time,
        sweep_type,
        operation,
        shots,
        sweeps,
        triggertype,
        triggerSource,
        extInThreshold,
    ):
        """
        Configures the built-in signal generator with the specified parameters.

        Args:
            offset (int): The DC offset of the waveform in microvolts.
            pk_to_pk (int): The peak-to-peak amplitude of the waveform in microvolts.
            wave_type (int): The waveform type (sine, square, etc.).
            start_frequency (float): The initial frequency of the waveform in Hz.
            stop_frequency (float): The final frequency of the waveform in Hz.
            increment (float): The frequency increment between start and stop frequencies in Hz.
            dwell_time (float): The time in seconds the waveform will stay at each frequency step during a sweep.
            sweep_type (int): The sweep type (up, down, up-down, or down-up).
            operation (int): The operation of the sweep (single or continuous).
            shots (int): The number of times the sweep will be triggered.
            sweeps (int): The number of sweeps to perform.
            triggertype (int): The trigger type (none, external, or software).
            triggerSource (int): The trigger source (channel A, channel B, external, or software).
            extInThreshold (int): The external trigger voltage threshold in millivolts.
        """
        wave_type = ctypes.c_int16(wave_type)
        sweep_type = ctypes.c_int32(sweep_type)
        triggertype = ctypes.c_int32(triggertype)
        triggerSource = ctypes.c_int32(triggerSource)
        assert_pico_ok(
            ps.ps2000aSetSigGenBuiltIn(
                self.chandle,
                offset,
                pk_to_pk,
                wave_type,
                start_frequency,
                stop_frequency,
                increment,
                dwell_time,
                sweep_type,
                operation,
                shots,
                sweeps,
                triggertype,
                triggerSource,
                extInThreshold,
            )
        )

    def set_sig_gen_arb(
        self,
        offset,
        pk_to_pk,
        start_delta_phase,
        stop_delta_phase,
        delta_phase_increment,
        dwell_count,
        waveform_data,
        waveform_size,
        sweep_type,
        operation,
        index_mode,
        shots,
        sweeps,
        triggertype,
        triggerSource,
        extInThreshold,
    ):
        """
        Configures the arbitrary waveform generator with the specified parameters.

        Args:
            offset (int): The DC offset of the waveform in microvolts.
            pk_to_pk (int): The peak-to-peak amplitude of the waveform in microvolts.
            start_delta_phase (int): The initial delta phase value.
            stop_delta_phase (int): The final delta phase value.
            delta_phase_increment (int): The delta phase increment between start and stop delta phase values.
            dwell_count (int): The number of waveform cycles to output at each delta phase increment.
            waveform_data (numpy.ndarray): The array containing the waveform data.
            waveform_size (int): The size of the waveform data array.
            sweep_type (int): The sweep type (up, down, up-down, or down-up).
            operation (int): The operation of the sweep (single or continuous).
            index_mode (int): The index mode (single or dual).
            shots (int): The number of times the sweep will be triggered.
            sweeps (int): The number of sweeps to perform.
            triggertype (int): The trigger type (none, external, or software).
            triggerSource (int): The trigger source (channel A, channel B, external, or software).
            extInThreshold (int): The external trigger voltage threshold in millivolts.
        """
        sweep_type = ctypes.c_int32(sweep_type)
        triggertype = ctypes.c_int32(triggertype)
        triggerSource = ctypes.c_int32(triggerSource)
        assert_pico_ok(
            ps.ps2000aSetSigGenArbitrary(
                self.chandle,
                offset,
                pk_to_pk,
                start_delta_phase,
                stop_delta_phase,
                delta_phase_increment,
                dwell_count,
                waveform_data,
                waveform_size,
                sweep_type,
                operation,
                index_mode,
                shots,
                sweeps,
                triggertype,
                triggerSource,
                extInThreshold,
            )
        )

    def set_params(
        self,
        frequency,
        wave_type=None,
        offset=None,
        pk_to_pk=None,
        increment=None,
        dwell_time=None,
        sweep_type=None,
        operation=None,
        shots=None,
        sweeps=None,
        triggertype=None,
        triggerSource=None,
        extInThreshold=None,
        waveform_data=None,
        delta_phase_increment=None,
        dwell_count=None,
        index_mode=None,
    ):
        if wave_type is not None:
            self.wave_type = wave_type
        if offset is not None:
            self.offset = offset
        if pk_to_pk is not None:
            self.pk_to_pk = pk_to_pk
        if len(np.atleast_1d(frequency)) == 1:
            self.start_frequency = frequency
            self.stop_frequency = frequency
        elif len(np.atleast_1d(frequency)) == 2:
            self.start_frequency = frequency[0]
            self.stop_frequency = frequency[1]
        if increment is not None:
            self.increment = increment
        if dwell_time is not None:
            self.dwell_time = dwell_time
        if sweep_type is not None:
            self.sweep_type = sweep_type
        if operation is not None:
            self.operation = operation
        if shots is not None:
            self.shots = shots
        if sweeps is not None:
            self.sweeps = sweeps
        if triggertype is not None:
            self.triggertype = triggertype
        if triggerSource is not None:
            self.triggerSource = triggerSource
        if extInThreshold is not None:
            self.extInThreshold = extInThreshold
        if index_mode is not None:
            self.index_mode = index_mode
        if delta_phase_increment is not None:
            self.delta_phase_increment = delta_phase_increment
        if dwell_count is not None:
            self.dwell_count = dwell_count

        if waveform_data is None:
            self.set_sig_gen_built_in(
                self.offset,
                self.pk_to_pk,
                self.wave_type,
                self.start_frequency,
                self.stop_frequency,
                self.increment,
                self.dwell_time,
                self.sweep_type,
                self.operation,
                self.shots,
                self.sweeps,
                self.triggertype,
                self.triggerSource,
                self.extInThreshold,
            )

        else:
            waveform_size = len(waveform_data)
            dds_freq = 48 * 10**6
            awgBufferSize = 4096
            phaseAccumulatorSize = 2**32
            start_delta_phase = round(
                self.start_frequency
                / dds_freq
                * phaseAccumulatorSize
                * waveform_size
                / awgBufferSize
                * 1.2025695931477516
            )
            stop_delta_phase = round(
                self.stop_frequency
                / dds_freq
                * phaseAccumulatorSize
                * waveform_size
                / awgBufferSize
                * 1.2025695931477516
            )
            print(start_delta_phase, stop_delta_phase)
            self.waveform_data = waveform_data
            self.set_sig_gen_arb(
                self.offset,
                self.pk_to_pk,
                start_delta_phase,
                stop_delta_phase,
                self.delta_phase_increment,
                self.dwell_count,
                self.waveform_data,
                waveform_size,
                self.sweep_type,
                self.operation,
                self.index_mode,
                self.shots,
                self.sweeps,
                self.triggertype,
                self.triggerSource,
                self.extInThreshold,
            )

    def set_frequency(self, new_freq):
        self.start_frequency = new_freq
        self.set_params(start_frequency=new_freq)

    def set_wave_type(self, new_wave_type):
        self.wave_type = new_wave_type
        self.set_params(wave_type=new_wave_type)

    def set_pk_to_pk(self, new_pk_to_pk):
        self.pk_to_pk = new_pk_to_pk
        self.set_params(pk_to_pk=new_pk_to_pk)

    def set_offset(self, new_offset):
        self.offset = new_offset
        self.set_params(offset=new_offset)

    def set_increment(self, new_increment):
        self.increment = new_increment
        self.set_params(increment=new_increment)

    def set_dwell_time(self, new_dwell_time):
        self.dwell_time = new_dwell_time
        self.set_params(dwell_time=new_dwell_time)

    def set_sweep_type(self, new_sweep_type):
        self.sweep_type = new_sweep_type
        self.set_params(sweep_type=new_sweep_type)

    def set_operation(self, new_operation):
        self.operation = new_operation
        self.set_params(operation=new_operation)

    def set_shots(self, new_shots):
        self.shots = new_shots
        self.set_params(shots=new_shots)

    def set_sweeps(self, new_sweeps):
        self.sweeps = new_sweeps
        self.set_params(sweeps=new_sweeps)

    def set_triggertype(self, new_triggertype):
        self.triggertype = new_triggertype
        self.set_params(triggertype=new_triggertype)

    def set_triggerSource(self, new_triggerSource):
        self.triggerSource = new_triggerSource
        self.set_params(triggerSource=new_triggerSource)

    def set_extInThreshold(self, new_extInThreshold):
        self.extInThreshold = new_extInThreshold
        self.set_params(extInThreshold=new_extInThreshold)

    def set_index_mode(self, new_index_mode):
        self.index_mode = new_index_mode
        self.set_params(index_mode=new_index_mode)

    def set_delta_phase_increment(self, new_delta_phase_increment):
        self.delta_phase_increment = new_delta_phase_increment
        self.set_params(delta_phase_increment=new_delta_phase_increment)

    def set_dwell_count(self, new_dwell_count):
        self.dwell_count = new_dwell_count
        self.set_params(dwell_count=new_dwell_count)

    def set_waveform_data(self, new_waveform_data):
        self.waveform_data = new_waveform_data
        self.set_params(waveform_data=new_waveform_data)


class PicoOscilloscope:
    def __init__(self, chandle):
        self.chandle = chandle
        self.channel = 0  # channel A
        self.enabled = 1  # enabled
        self.coupling_type = 1  # DC
        self.channel_range = 6
        self.analogue_offset = 0
        self.timebase = 8
        self.num_samples = None
        self.oversample = 0
        self.segment_index = 0
        self.pre_trigger = None
        self.post_trigger = None
        self.start_index = 0
        self.ratio_mode = 0
        self.downsample_ratio = 0
        self.downsample_mode = 0
        self.threshold = 1024
        self.direction = 2  # rising direction
        self.delay = 0
        self.auto_trigger_ms = 0

    def set_params(
        self,
        channel_change=False,
        channel=None,
        enabled=None,
        coupling_type=None,
        channel_range=None,
        analogue_offset=None,
        timebase=None,
        num_samples=None,
        oversample=None,
        segment_index=None,
        pre_trigger=None,
        post_trigger=None,
        start_index=None,
        ratio_mode=None,
        downsample_ratio=None,
        downsample_mode=None,
        threshold=None,
        direction=None,
        delay=None,
        auto_trigger_ms=None,
    ):
        """
        Set parameters for the PicoOscilloscope.
        Args:
        channel_change (bool): indicates whether the channel has changed
        channel (int): channel number (0 for channel A, 1 for channel B)
        enabled (int): 1 for enabled, 0 for disabled
        coupling_type (int): 1 for DC coupling, 0 for AC coupling
        channel_range (int): voltage range of the channel
        analogue_offset (float): offset voltage in millivolts
        timebase (int): time between each sample, 2**(timebase - 1) ns
        num_samples (int): number of samples to collect
        oversample (int): oversampling factor
        segment_index (int): index of the memory segment to use
        pre_trigger (int): number of samples before the trigger event
        post_trigger (int): number of samples after the trigger event
        start_index (int): index of the first sample to return
        ratio_mode (int): ratio mode for downsampling; 0 for None, 1 for Aggregate, 2 for Decimate, 3 for Average
        downsample_ratio (int): downsampling ratio
        downsample_mode (int): downsampling mode; 0 for None, 1 for Simple, 2 for Peak Detection
        threshold (int): threshold for the trigger event (adc counts currently)
        direction (int): direction of the trigger event; 0 for Rising, 1 for Falling, 2 for Rising or Falling
        delay (int): delay in samples from the trigger event
        auto_trigger_ms (int): timeout in milliseconds for auto trigger
        """
        if channel is not None:
            self.channel = channel
            channel_change = True
        if enabled is not None:
            self.enabled = enabled
            channel_change += 1
        if coupling_type is not None:
            self.coupling_type = coupling_type
            channel_change = True
        if channel_range is not None:
            self.channel_range = channel_range
            channel_change = True
        if analogue_offset is not None:
            self.analogue_offset = analogue_offset
            channel_change = True
        if timebase is not None:
            self.timebase = timebase
        if num_samples is not None:
            self.num_samples = num_samples
        if oversample is not None:
            self.oversample = oversample
        if segment_index is not None:
            self.segment_index = segment_index
        if pre_trigger is not None:
            self.pre_trigger = pre_trigger
        if post_trigger is not None:
            self.post_trigger = post_trigger
        if start_index is not None:
            self.start_index = start_index
        if ratio_mode is not None:
            self.ratio_mode = ratio_mode
        if downsample_ratio is not None:
            self.downsample_ratio = downsample_ratio
        if downsample_mode is not None:
            self.downsample_mode = downsample_mode
        if threshold is not None:
            self.threshold = threshold
        if direction is not None:
            self.direction = direction
        if delay is not None:
            self.delay = delay
        if auto_trigger_ms is not None:
            self.auto_trigger_ms = auto_trigger_ms
        if channel_change:
            self.set_channel()

    def set_channel(self):
        """
        Configure the oscilloscope channel settings according to the current parameters.
        """
        assert_pico_ok(
            ps.ps2000aSetChannel(
                self.chandle,
                self.channel,
                self.enabled,
                self.coupling_type,
                self.channel_range,
                self.analogue_offset,
            )
        )

    def set_trigger(self):
        """
        Configure the oscilloscope trigger settings according to the current parameters.
        """
        assert_pico_ok(
            ps.ps2000aSetSimpleTrigger(
                self.chandle,
                self.enabled,
                self.channel,
                self.threshold,
                self.direction,
                self.delay,
                self.auto_trigger_ms,
            )
        )

    def get_timebase(self):
        """
        Get the time interval in nanoseconds between samples and return its value.
        Returns:
            float: Time interval in nanoseconds between samples.
        """
        time_interval_ns = ctypes.c_float()
        time_units = ctypes.c_int16()
        max_samples = ctypes.c_int32()
        assert_pico_ok(
            ps.ps2000aGetTimebase2(
                self.chandle,
                self.timebase,
                self.num_samples,
                ctypes.byref(time_interval_ns),
                self.oversample,
                ctypes.byref(max_samples),
                0,
            )
        )
        return time_interval_ns.value

    def set_sampling_rate(self, frequency, peaks_wanted=5):
        """
        Set the sampling rate based on the given frequency and the number of peaks wanted.
        Args:
            frequency (float): The signal frequency.
            peaks_wanted (int, optional): The number of peaks to capture. Defaults to 5.
        """
        period = 1 / frequency
        time_interval_s = 2 ** (self.timebase + 1) * 1e-9
        new_sampling_rate = int(peaks_wanted * period / time_interval_s)
        self.pre_trigger = int(new_sampling_rate / 2)
        self.post_trigger = int(new_sampling_rate / 2)
        self.num_samples = new_sampling_rate
        self.set_params(
            pre_trigger=self.pre_trigger,
            post_trigger=self.post_trigger,
            num_samples=self.num_samples,
        )

    def run_block(self):
        """
        Start the oscilloscope to run a block mode data acquisition.
        """
        assert_pico_ok(
            ps.ps2000aRunBlock(
                self.chandle,
                self.pre_trigger,
                self.post_trigger,
                self.timebase,
                self.oversample,
                None,
                0,
                None,
                None,
            )
        )

    def set_data_buffers(self):
        """
        Set the data buffers to store the acquired data from the oscilloscope.
        """
        self.bufferMax = (ctypes.c_int16 * self.num_samples)()
        self.bufferMin = (ctypes.c_int16 * self.num_samples)()
        assert_pico_ok(
            ps.ps2000aSetDataBuffers(
                self.chandle,
                self.channel,
                ctypes.byref(self.bufferMax),
                ctypes.byref(self.bufferMin),
                self.num_samples,
                self.segment_index,
                self.ratio_mode,
            )
        )

    def is_ready(self):
        ready = ctypes.c_int16(0)
        assert_pico_ok(ps.ps2000aIsReady(self.chandle, ctypes.byref(ready)))
        return bool(ready.value)

    def get_values(self):
        """
        Retrieve the acquired data from the oscilloscope.

        Returns:
            tuple: A tuple containing the number of actual samples (int) and overflow status (int).
        """
        actual_samples = ctypes.c_int32(self.num_samples)
        overflow = ctypes.c_int16()
        assert_pico_ok(
            ps.ps2000aGetValues(
                self.chandle,
                self.start_index,
                ctypes.byref(actual_samples),
                self.downsample_ratio,
                self.downsample_mode,
                0,
                ctypes.byref(overflow),
            )
        )
        return actual_samples.value, overflow.value

    def get_adc_to_mv(self):
        """
        Convert the acquired data from ADC counts to millivolts.
        Returns:
            list: A list of acquired data in millivolts.
        """
        maxADC = ctypes.c_int16()
        assert_pico_ok(ps.ps2000aMaximumValue(self.chandle, ctypes.byref(maxADC)))
        adc_to_mv = adc2mV(self.bufferMax, self.channel_range, maxADC)
        return adc_to_mv, maxADC.value

    def calculate_pulselength(self, mV, time_axis):
        threshold = np.max(mV) / 2
        high_voltage_regions = np.where(mV > threshold)[0]
        high_lengths = np.split(
            high_voltage_regions, np.where(np.diff(high_voltage_regions) != 1)[0] + 1
        )
        high_lengths = [len(region) for region in high_lengths]
        longest_region = max(high_lengths)
        pulse_length = longest_region * (time_axis[1] - time_axis[0])
        # find low voltage length
        low_voltage_regions = np.where(mV < threshold)[0]
        low_lengths = np.split(
            low_voltage_regions, np.where(np.diff(low_voltage_regions) != 1)[0] + 1
        )
        low_lengths = [len(region) for region in low_lengths]
        longest_region = max(low_lengths)
        pulse_dist = longest_region * (time_axis[1] - time_axis[0])
        return pulse_length, pulse_dist

    def run_scope(self):
        """
        Run the oscilloscope, wait for data acquisition, and retrieve the results.
        Returns:
            tuple: A tuple containing the time axis (numpy array), acquired data in millivolts (list), and overflow status (int).
        """
        self.run_block()
        while not self.is_ready():
            pass
        self.set_data_buffers()
        samples, overflow = self.get_values()
        mV, maxADC = self.get_adc_to_mv()
        time_interval_us = self.get_timebase() * 1e-3
        time_axis = np.linspace(0, time_interval_us * samples, self.num_samples)
        pulse_length, pulse_dist = self.calculate_pulselength(mV, time_axis)
        return time_axis, mV, overflow, maxADC, pulse_length, pulse_dist


class PicoScope2000a:
    def __init__(self):
        self.chandle = ctypes.c_int16()
        status = {}
        assert_pico_ok(ps.ps2000aOpenUnit(ctypes.byref(self.chandle), None))
        self.oscilloscope = PicoOscilloscope(self.chandle)
        self.awg = PicoAWG(self.chandle)

    def close(self):
        assert_pico_ok(ps.ps2000aCloseUnit(self.chandle))
