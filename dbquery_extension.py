from datetime import timedelta, datetime
from pathlib import Path
import random

from ruxit.api.base_plugin import RemoteBasePlugin


class CustomDBQueryPluginRemote(RemoteBasePlugin):
    def query(self, **kwargs):
        self.logger.setLevel(self.config.get("log_level"))

        self.logger.info(("Starting new DEMO cycle..."))
        self.logger.debug(("Creating custom devices..."))

        group = self.topology_builder.create_group("QREP CAS", "QREP CAS")
        self.custom_device_apply = group.create_device(
            "QREP CAS apply", "QREP CAS apply"
        )
        self.custom_device_capture = group.create_device(
            "QREP CAS capture", "QREP CAS capture"
        )

        # Simulate good and bad values
        # Generate values 0 == bad
        apply_depth = random.randint(0, 10)
        capture_depth = random.randint(0, 10)

        self.logger.info(("Starting apply run..."))
        self.logger.debug(("Apply depth: %s" % apply_depth))
        # Apply Script
        if apply_depth == 0:
            # Simulate bad values
            self.logger.info(("Apply depth is 0, simulating bad values..."))

            apply_depth = random.randint(165, 287)
            self.logger.debug(("New error apply qdepth: %s" % apply_depth))

            self.logger.debug(("Reporting Metrics..."))

            self.custom_device_apply.absolute(
                "qrep.cas.apply.queue.depth",
                apply_depth,
                {"queue": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001"},
            )

            apply_depth2 = apply_depth - random.randint(80, 150)
            self.custom_device_apply.absolute(
                "qrep.cas.apply.queue.depth",
                apply_depth2,
                {"queue": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L002"},
            )

            self.logger.debug(("Reporting Events..."))

            self.custom_device_apply.report_error_event(
                title="Recive Queue DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001",
                description="A-RQU ERROR",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "A-RQU",
                    "SEV": "ERROR",
                    "QUEUE": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001",
                    "MTXT": "Recive Queue DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001 aktiv (#subs A/I/O): 0/0/0. QDEPTH=%s (0%) OLDEST_TRANS=2023-08-07-11.51.37.000000 MEMORY=0/256mb."
                    % apply_depth,
                },
            )

            latency = random.randint(605, 1816)
            self.custom_device_apply.report_error_event(
                title="Apply End2End Latenz Problem",
                description="A-LAT ERROR",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "A-LAT",
                    "SEV": "ERROR",
                    "THRESHOLD": "< 600s",
                    "QUEUE": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001",
                    "MTXT": "Q Apply End2End Latenz ERROR (End2End Latency < 600s) fuer DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001 (E2E=%ss, C=0.0s, A=0.0s, Q=0.0s), QDEPTH=0 (0%), ROW_APPLIED=0"
                    % latency,
                },
            )

            self.custom_device_apply.report_custom_info_event(
                title="Heartbeat ok",
                description="A-CHB Info",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "A-CHB",
                    "SEV": "INFO",
                    "QUEUE": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001",
                    "MTXT": "10 Heartbeat Messages fuer Queue DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001 in den letzten 10 Minuten.",
                },
            )

            self.custom_device_apply.report_custom_info_event(
                title="Recive Queue DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L002",
                description="A-RQU WARNING",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "A-RQU",
                    "SEV": "WARNING",
                    "QUEUE": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L002",
                    "MTXT": "Recive Queue DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L002 aktiv (#subs A/I/O): 5/0/0. QDEPTH=%s (0%) OLDEST_TRANS=2023-08-07-11.51.37.000000 MEMORY=0/256mb."
                    % apply_depth2,
                },
            )

            self.custom_device_apply.report_custom_info_event(
                title="Apply End2End Latenz ok",
                description="A-LAT Info",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "A-LAT",
                    "SEV": "INFO",
                    "THRESHOLD": "< 600s",
                    "QUEUE": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L002",
                    "MTXT": "Q Apply End2End Latenz ok (End2End Latency < 600s) fuer DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L002 (E2E=0.0s, C=0.0s, A=0.0s, Q=0.0s), QDEPTH=0 (0%), ROW_APPLIED=0",
                },
            )

            self.custom_device_apply.report_custom_info_event(
                title="Heartbeat ok",
                description="A-CHB Info",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "A-CHB",
                    "SEV": "INFO",
                    "QUEUE": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L002",
                    "MTXT": "10 Heartbeat Messages fuer Queue DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L002 in den letzten 10 Minuten.",
                },
            )

            # Report event count metrics
            self.logger.info("Reporting event count metrics...")
            self.custom_device_apply.absolute(
                "qrep.cas.apply.events.count",
                2,
                {"severity": "ERROR"},
            )

            self.custom_device_apply.absolute(
                "qrep.cas.apply.events.count",
                1,
                {"severity": "WARNING"},
            )

            self.custom_device_apply.absolute(
                "qrep.cas.apply.events.count",
                3,
                {"severity": "INFO"},
            )

        else:
            # Simulate good values
            self.logger.info("Reporting good values...")

            self.logger.debug("Reporting metrics...")
            self.custom_device_apply.absolute(
                "qrep.cas.apply.queue.depth",
                0,
                {"queue": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001"},
            )

            self.custom_device_apply.absolute(
                "qrep.cas.apply.queue.depth",
                0,
                {"queue": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L002"},
            )

            self.logger.debug("Reporting events...")
            self.custom_device_apply.report_custom_info_event(
                title="Recive Queue DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001",
                description="A-RQU Info",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "A-RQU",
                    "SEV": "INFO",
                    "QUEUE": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001",
                    "MTXT": "Recive Queue DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001 aktiv (#subs A/I/O): 0/0/0. QDEPTH=0 (0%) OLDEST_TRANS=2023-08-07-11.51.37.000000 MEMORY=0/256mb.",
                },
            )

            self.custom_device_apply.report_custom_info_event(
                title="Apply End2End Latenz ok",
                description="A-LAT Info",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "A-LAT",
                    "SEV": "INFO",
                    "THRESHOLD": "< 600s",
                    "QUEUE": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001",
                    "MTXT": "Q Apply End2End Latenz ok (End2End Latency < 600s) fuer DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001 (E2E=0.0s, C=0.0s, A=0.0s, Q=0.0s), QDEPTH=0 (0%), ROW_APPLIED=0",
                },
            )

            self.custom_device_apply.report_custom_info_event(
                title="Heartbeat ok",
                description="A-CHB Info",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "A-CHB",
                    "SEV": "INFO",
                    "QUEUE": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001",
                    "MTXT": "10 Heartbeat Messages fuer Queue DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001 in den letzten 10 Minuten.",
                },
            )

            self.custom_device_apply.report_custom_info_event(
                title="Recive Queue DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L002",
                description="A-RQU Info",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "A-RQU",
                    "SEV": "INFO",
                    "QUEUE": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L002",
                    "MTXT": "Recive Queue DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L002 aktiv (#subs A/I/O): 5/0/0. QDEPTH=0 (0%) OLDEST_TRANS=2023-08-07-11.51.37.000000 MEMORY=0/256mb.",
                },
            )

            self.custom_device_apply.report_custom_info_event(
                title="Apply End2End Latenz ok",
                description="A-LAT Info",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "A-LAT",
                    "SEV": "INFO",
                    "THRESHOLD": "< 600s",
                    "QUEUE": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L002",
                    "MTXT": "Q Apply End2End Latenz ok (End2End Latency < 600s) fuer DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L002 (E2E=0.0s, C=0.0s, A=0.0s, Q=0.0s), QDEPTH=0 (0%), ROW_APPLIED=0",
                },
            )

            self.custom_device_apply.report_custom_info_event(
                title="Heartbeat ok",
                description="A-CHB Info",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "A-CHB",
                    "SEV": "INFO",
                    "QUEUE": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L002",
                    "MTXT": "10 Heartbeat Messages fuer Queue DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L002 in den letzten 10 Minuten.",
                },
            )

            self.logger.debug("Reporting event metrics...")
            self.custom_device_apply.absolute(
                "qrep.cas.apply.events.count",
                6,
                {"severity": "INFO"},
            )

        # Capture Script
        self.logger.info("Starting capture script...")
        self.logger.debug("capture_depth: %s" % capture_depth)

        if capture_depth == 0:
            # Simulate bad values
            self.logger.info("Reporting bad values...")

            latency = random.randint(516, 1091)
            self.logger.debug("Error latency: %s" % latency)

            self.logger.debug("Reporting events...")
            self.custom_device_capture.report_error_event(
                title="Capture Latenz Problem",
                description="A-LAT ERROR",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "A-LAT",
                    "SEV": "ERROR",
                    "THRESHOLD": "< 500s",
                    "QUEUE": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001",
                    "MTXT": "Q Capture Latenz ERROR (Capture Latency < 500s). Capture Latency=%s s, MEMORY: 0/0MB, TRANS_SPILLED=0"
                    % latency,
                },
            )

            self.custom_device_capture.report_custom_info_event(
                title="Send Queue CAS1I1E.L001 aktiv",
                description="C-SQU INFO",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "C-SQU",
                    "SEV": "INFO",
                    "QUEUE": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001",
                    "MTXT": "Send Queue DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001 aktiv. (#subs A/I/N/O: 0/0/0/0). XMITQDEPTH=0",
                },
            )

            self.custom_device_capture.report_error_event(
                title="Send Queue S100SE5I.L001 ERROR",
                description="C-SQU ERROR",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "C-SQU",
                    "SEV": "ERROR",
                    "QUEUE": "DB2.QREP.IDRO.RECVQ.DB2T.S100SE5I.L001",
                    "MTXT": "Send Queue DB2.QREP.IDRO.RECVQ.DB2T.S100SE5I.L001 ERROR. (#subs A/I/N/O: 4/0/0/0). XMITQDEPTH=0",
                },
            )

            self.custom_device_capture.report_custom_info_event(
                title="Subscriptions Send Queue S100SE5I.L001 aktiv",
                description="C-SUB WARNING",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "C-SUB",
                    "SEV": "WARNING",
                    "QUEUE": "DB2.QREP.IDRO.RECVQ.DB2T.S100SE5I.L001",
                    "MTXT": "Nicht alle relevanten 4 Subscriptions fuer SENDQ DB2.QREP.IDRO.RECVQ.DB2T.S100SE5I.L001 sind aktiv!",
                },
            )

            self.custom_device_capture.report_custom_info_event(
                title="Subscriptions Send Queue CAS1T1E.L001 aktiv",
                description="C-SUB INFO",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "C-SUB",
                    "SEV": "INFO",
                    "QUEUE": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001",
                    "MTXT": "Alle relevanten 5 Subscriptions fuer SENDQ DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001 aktiv.",
                },
            )

            # Report event count metrics
            self.logger.debug("Reporting event metrics...")
            self.custom_device_capture.absolute(
                "qrep.cas.capture.events.count",
                2,
                {"severity": "ERROR"},
            )

            self.custom_device_capture.absolute(
                "qrep.cas.capture.events.count",
                1,
                {"severity": "WARNING"},
            )

            self.custom_device_capture.absolute(
                "qrep.cas.capture.events.count",
                2,
                {"severity": "INFO"},
            )

        else:
            # Simulate good values
            self.logger.info("Reporting good values...")
            latency = random.randint(0, 5)
            self.logger.debug("Latency: %s" % latency)

            self.logger.debug("Reporting events...")
            self.custom_device_capture.report_custom_info_event(
                title="Capture Latenz ok",
                description="A-LAT Info",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "A-LAT",
                    "SEV": "INFO",
                    "THRESHOLD": "< 500s",
                    "QUEUE": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001",
                    "MTXT": "Q Capture Latenz ERROR (Capture Latency < 500s). Capture Latency=%s s, MEMORY: 0/0MB, TRANS_SPILLED=0"
                    % latency,
                },
            )

            self.custom_device_capture.report_custom_info_event(
                title="Send Queue CAS1I1E.L001 aktiv",
                description="C-SQU INFO",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "C-SQU",
                    "SEV": "INFO",
                    "QUEUE": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001",
                    "MTXT": "Send Queue DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001 aktiv. (#subs A/I/N/O: 0/0/0/0). XMITQDEPTH=0",
                },
            )

            self.custom_device_capture.report_custom_info_event(
                title="Send Queue S100SE5I.L001 aktiv",
                description="C-SQU INFO",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "C-SQU",
                    "SEV": "INFO",
                    "QUEUE": "DB2.QREP.IDRO.RECVQ.DB2T.S100SE5I.L001",
                    "MTXT": "Send Queue DB2.QREP.IDRO.RECVQ.DB2T.S100SE5I.L001 aktiv. (#subs A/I/N/O: 4/0/0/0). XMITQDEPTH=0",
                },
            )

            self.custom_device_capture.report_custom_info_event(
                title="Subscriptions Send Queue S100SE5I.L001 aktiv",
                description="C-SUB INFO",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "C-SUB",
                    "SEV": "INFO",
                    "QUEUE": "DB2.QREP.IDRO.RECVQ.DB2T.S100SE5I.L001",
                    "MTXT": "Alle relevanten 4 Subscriptions fuer SENDQ DB2.QREP.IDRO.RECVQ.DB2T.S100SE5I.L001 aktiv.",
                },
            )

            self.custom_device_capture.report_custom_info_event(
                title="Subscriptions Send Queue CAS1T1E.L001 aktiv",
                description="C-SUB INFO",
                properties={
                    "Program": "ASNQAPP(G00)",
                    "Current Server": "CAS1T1E",
                    "MTYP": "C-SUB",
                    "SEV": "INFO",
                    "QUEUE": "DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001",
                    "MTXT": "Alle relevanten 5 Subscriptions fuer SENDQ DB2.QREP.IDRC.RECVQ.DB2T.CAS1T1E.L001 aktiv.",
                },
            )

            self.logger.debug("Reporting event metrics...")
            self.custom_device_capture.absolute(
                "qrep.cas.capture.events.count",
                5,
                {"severity": "INFO"},
            )

        self.logger.debug("Reporting exception metrics...")
        self.custom_device_apply.report_custom_info_event(
            title="Exceptions ok",
            description="Keine Exceptions in den letzten 24 Stunden.",
            properties={
                "Program": "ASNQCAP(DB2IDRO)",
                "Current Server": "CAS1T1E",
                "MTYP": "A-EXC",
                "SEV": "INFO",
                "MTXT": "Keine Exceptions in den letzten 24 Stunden.",
            },
        )
