package com.example.cinysarmorhud;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.rendering.v1.hud.HudElementRegistry;
import net.fabricmc.fabric.api.client.rendering.v1.hud.VanillaHudElements;
import net.minecraft.resources.Identifier;

public class CinysArmorHudClient implements ClientModInitializer {
    public static final String MOD_ID = "cinysarmorhud";

    @Override
    public void onInitializeClient() {
        HudElementRegistry.attachElementBefore(
            VanillaHudElements.CHAT,
            Identifier.fromNamespaceAndPath(MOD_ID, "cinys_armor_hud"),
            CinysArmorHud::render
        );
    }
}
