package com.example.cinysarmorhud;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.rendering.v1.HudRenderCallback;

public class CinysArmorHudClient implements ClientModInitializer {
    public static final String MOD_ID = "cinysarmorhud";

    @Override
    public void onInitializeClient() {
        HudRenderCallback.EVENT.register((graphics, deltaTracker) -> CinysArmorHud.render(graphics));
    }
}
