# ciny's armor HUD (chess.com)

Client-side Fabric mod. A four-slot armor strip left of the hotbar, drawn from the vanilla hotbar texture.
Items and the durability bar are drawn by the game itself (identical to the inventory; the bar is hidden while
the piece is undamaged). Each damageable piece gets a 8x8 pixel move-review badge (same size and octagon shape as uku's warning icon) above it.
Layout numbers were taken from uku's Armor HUD; no code was copied. Inspired by uku's Armor HUD (MIT) and
BerdinskiyBear's original.

| Remaining durability | Rating      |
|----------------------|-------------|
| 76-100 %             | Brilliant (!!)  |
| 51-75 %              | Best Move (star)|
| 26-50 %              | Inaccuracy (?!) |
| 1-25 %               | Blunder (??)    |

Two separate projects:
- `fabric-1.21.11/` - Minecraft 1.21.11, Java 21, Mojang mappings, `HudElementRegistry`
- `fabric-1.21/`  - Minecraft 1.21 / 1.21.1, Java 21, Mojang mappings, `HudRenderCallback`
- `fabric-26.3/`  - Minecraft 26.3, Java 25, unobfuscated, `HudElementRegistry`

## Build
1. Add a Gradle wrapper (copy `gradlew`, `gradlew.bat`, `gradle/` from the official Fabric template
   generator at https://fabricmc.net/develop/template/ , or run `gradle wrapper` with Gradle installed).
   1.21 needs Gradle 8.12+, 26.3 needs Gradle 9.x.
2. `./gradlew build` -> jar in `build/libs/`. `./gradlew runClient` to test in dev.

## Badges
`make_badges.py` regenerates the 16x16 pixel badges (original artwork, Pillow required).
All thresholds live in `Rating.java`; layout constants are at the top of `CinysArmorHud.java`.

## Testing
Dev client (easiest): JDK 21 for `fabric-1.21`, JDK 25 for `fabric-26.3`, then in that folder run
`./gradlew runClient` (`gradlew.bat runClient` on Windows). Make a Creative world with cheats on and run:

    /item replace entity @s armor.head with diamond_helmet[damage=300]    -> Blunder    (~17 % left)
    /item replace entity @s armor.chest with iron_chestplate[damage=150]  -> Inaccuracy (~37 % left)
    /item replace entity @s armor.legs with diamond_leggings[damage=180]  -> Best Move  (~64 % left)
    /item replace entity @s armor.feet with diamond_boots[damage=0]       -> Brilliant, no bar

Real install: `./gradlew build`, then put `build/libs/cinys-armor-hud-*.jar` (not the -sources jar) in your
`mods` folder together with Fabric API, using a Fabric profile for the matching Minecraft version.

## Easiest way to get the jar (no Java, no Gradle wrapper)
Upload this whole folder to a new GitHub repo (keep `.github/workflows/build.yml`). GitHub builds both jars for you:
repo -> Actions -> "Build mod jars" -> Run workflow -> open the finished run -> download `fabric-1.21.11-jar` (Minecraft 1.21.11), `fabric-1.21-jar` (1.21/1.21.1) or `fabric-26.3-jar`.
On Modrinth, list Fabric API as a *required dependency* so players get it automatically with one click.
