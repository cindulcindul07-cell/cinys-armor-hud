package com.example.cinysarmorhud;

import net.minecraft.resources.ResourceLocation;

/** Move-review style rating for an armor piece, based on remaining durability. */
public enum Rating {
    BRILLIANT("brilliant"),     // 76-100 %
    BEST_MOVE("best_move"),     // 51-75 %
    INACCURACY("inaccuracy"),   // 26-50 %
    BLUNDER("blunder");         // 1-25 %

    public final ResourceLocation texture;

    Rating(String file) {
        this.texture = ResourceLocation.fromNamespaceAndPath(CinysArmorHudClient.MOD_ID, "textures/gui/" + file + ".png");
    }

    public static Rating fromRemainingPercent(double percent) {
        if (percent > 75) return BRILLIANT;
        if (percent > 50) return BEST_MOVE;
        if (percent > 25) return INACCURACY;
        return BLUNDER;
    }
}
