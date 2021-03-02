logos = {"bazarr": "https://i.imgur.com/reWArsB.png", "bitwarden": "https://i.imgur.com/7ziLQf9.png",
         "postgres": "https://i.imgur.com/GhkyvuT.png", "booksonic": "https://i.imgur.com/87KtEu1.png",
         "jackett": "https://i.imgur.com/Lz06x5b.png", "mariadb": "https://i.imgur.com/rpInfpg.png",
         "netdata": "https://i.imgur.com/kzLB8ou.png", "nextcloud": "https://i.imgur.com/n0sUUPo.png",
         "ombi": "https://i.imgur.com/dKJ3ECe.png", "organizr": "https://i.imgur.com/qJZ1kP5.png",
         "pihole": "https://i.imgur.com/IvLTuKF.png", "plex": "https://i.imgur.com/KtLTu8y.png",
         "portainer": "https://i.imgur.com/61ODRl3.png", "qbittorrent": "https://i.imgur.com/SmDt1PA.png",
         "radarr": "https://i.imgur.com/C4usmjf.png", "sonarr": "https://i.imgur.com/e4qj98C.png",
         "tautulli": "https://i.imgur.com/8XCuIQ8.png", "watchtower": "https://i.imgur.com/kiALl1f.png",
         "wiki": "https://i.imgur.com/2yfdYWt.png", "swag": "https://i.imgur.com/EJ1pOeM.png"}


def getLogoUrl(name):
    onlyImage = name.split(":")[0].lower()
    for kl, vl in logos.items():
        if kl.find(onlyImage) != -1:
            return vl

    return "https://i.imgur.com/J8k42gI.png"
