import subprocess, os
import CloudFlare

try:
    import config
except:
    import config_example as config

def main() -> None:
    try:
        cfadapter = CloudFlare.CloudFlare(token=config.TOKEN)
        zones = cfadapter.zones.get(params={"name": config.ZONE})

        if not zones:
            print("Cannot get this Zone. Are your credentials correct?")
            os.exit(1)

        aaaa_record = cfadapter.zones.dns_records.get(
            zones[0]["id"],
            params={
                "name": "{}.{}".format(config.RECORD, config.ZONE),
                "match": "all",
                "type": "AAAA",
            },
        )

        if not aaaa_record:
            print("There is no AAAA record for this zone.")
            os.exit(1)

        ipv6 = get_ipv6_address()

        if aaaa_record[0]["content"] != ipv6:
            cfadapter.zones.dns_records.put(
                zones[0]["id"],
                aaaa_record[0]["id"],
                data={
                    "name": aaaa_record[0]["name"],
                    "type": "AAAA",
                    "content": ipv6,
                    "proxied": aaaa_record[0]["proxied"],
                    "ttl": aaaa_record[0]["ttl"],
                },
            )
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        print("There was an error accessing the CloudFlare API: ", e)


def get_ipv6_address() -> str:
    return subprocess.check_output(config.ipcmd, shell=True).decode().strip().split(" ")[1][:-3]


if __name__ == "__main__":
    main()
