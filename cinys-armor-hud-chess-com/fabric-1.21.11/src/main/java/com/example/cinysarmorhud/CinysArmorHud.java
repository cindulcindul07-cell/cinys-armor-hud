package com.example.cinysarmorhud;

import net.minecraft.client.DeltaTracker;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.HumanoidArm;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.InventoryMenu;
import net.minecraft.world.item.ItemStack;

/**
 * Minecraft 1.21.11 version. Armor widget drawn from the vanilla hotbar texture; items, enchant glint,
 * trims, dye and the durability bar are drawn by the game itself, so they look exactly like in the inventory.
 * Layout numbers (step 20, size 22, offsets 98 / 29) mirror uku's Armor HUD.
 */
public final class CinysArmorHud {
    private static final EquipmentSlot[] SLOTS = {
        EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET
    };
    private static final Identifier[] EMPTY = {
        InventoryMenu.EMPTY_ARMOR_SLOT_HELMET, InventoryMenu.EMPTY_ARMOR_SLOT_CHESTPLATE,
        InventoryMenu.EMPTY_ARMOR_SLOT_LEGGINGS, InventoryMenu.EMPTY_ARMOR_SLOT_BOOTS
    };
    private static final Identifier HOTBAR =
        Identifier.withDefaultNamespace("textures/gui/sprites/hud/hotbar.png");

    private static final int STEP = 20, SIZE = 22, HOTBAR_OFFSET = 98, OFFHAND_OFFSET = 29, BADGE = 8;

    private CinysArmorHud() {}

    public static void render(GuiGraphics g, DeltaTracker deltaTracker) {
        Minecraft mc = Minecraft.getInstance();
        Player player = mc.player;
        if (player == null || player.isSpectator()) return;

        int sw = mc.getWindow().getGuiScaledWidth();
        int sh = mc.getWindow().getGuiScaledHeight();

        int width = SLOTS.length * STEP + 2;
        int rightEdge = sw / 2 - HOTBAR_OFFSET;
        if (player.getMainArm() == HumanoidArm.RIGHT && !player.getOffhandItem().isEmpty()) {
            rightEdge -= OFFHAND_OFFSET;
        }
        int x0 = rightEdge - width;
        int y0 = sh - SIZE;

        g.blit(RenderPipelines.GUI_TEXTURED, HOTBAR, x0, y0, 0f, 0f, width - 2, SIZE, 182, 22);
        g.blit(RenderPipelines.GUI_TEXTURED, HOTBAR, x0 + width - 2, y0, 180f, 0f, 2, SIZE, 182, 22);

        for (int i = 0; i < SLOTS.length; i++) {
            int sx = x0 + i * STEP;
            ItemStack stack = player.getItemBySlot(SLOTS[i]);

            if (stack.isEmpty()) {
                g.blitSprite(RenderPipelines.GUI_TEXTURED, EMPTY[i], sx + 3, y0 + 3, 16, 16);
                continue;
            }

            g.renderItem(stack, sx + 3, y0 + 3);
            g.renderItemDecorations(mc.font, stack, sx + 3, y0 + 3); // vanilla durability bar (hidden when undamaged)

            if (stack.isDamageableItem() && stack.getMaxDamage() > 0) {
                double remaining = 100.0 * (stack.getMaxDamage() - stack.getDamageValue()) / stack.getMaxDamage();
                Rating rating = Rating.fromRemainingPercent(remaining);
                g.blit(RenderPipelines.GUI_TEXTURED, rating.texture,
                    sx + 6, y0 - BADGE - 2, 0f, 0f, BADGE, BADGE, BADGE, BADGE);
            }
        }
    }
}
