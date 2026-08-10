"""
=========================================================
CyberScope Animations
Professional Animation Engine
Author : Krunal Paliwal
=========================================================
"""

from PyQt5.QtCore import (
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QParallelAnimationGroup,
)

from PyQt5.QtWidgets import (
    QGraphicsOpacityEffect,
    QGraphicsDropShadowEffect,
)

from PyQt5.QtGui import QColor


# ==========================================================
# Fade In
# ==========================================================

def fade_in(widget, duration=400):

    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b"opacity")

    animation.setDuration(duration)
    animation.setStartValue(0.0)
    animation.setEndValue(1.0)
    animation.setEasingCurve(QEasingCurve.OutCubic)

    animation.start()

    widget._fade_animation = animation

    return animation


# ==========================================================
# Fade Out
# ==========================================================

def fade_out(widget, duration=400):

    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b"opacity")

    animation.setDuration(duration)
    animation.setStartValue(1.0)
    animation.setEndValue(0.0)
    animation.setEasingCurve(QEasingCurve.OutCubic)

    animation.start()

    widget._fade_animation = animation

    return animation


# ==========================================================
# Slide From Left
# ==========================================================

def slide_from_left(widget, duration=500):

    end_pos = widget.pos()

    start_pos = QPoint(
        end_pos.x() - 120,
        end_pos.y()
    )

    widget.move(start_pos)

    animation = QPropertyAnimation(widget, b"pos")

    animation.setDuration(duration)

    animation.setStartValue(start_pos)

    animation.setEndValue(end_pos)

    animation.setEasingCurve(QEasingCurve.OutCubic)

    animation.start()

    widget._slide_animation = animation

    return animation


# ==========================================================
# Slide From Right
# ==========================================================

def slide_from_right(widget, duration=500):

    end_pos = widget.pos()

    start_pos = QPoint(
        end_pos.x() + 120,
        end_pos.y()
    )

    widget.move(start_pos)

    animation = QPropertyAnimation(widget, b"pos")

    animation.setDuration(duration)

    animation.setStartValue(start_pos)

    animation.setEndValue(end_pos)

    animation.setEasingCurve(QEasingCurve.OutCubic)

    animation.start()

    widget._slide_animation = animation

    return animation


# ==========================================================
# Slide From Bottom
# ==========================================================

def slide_from_bottom(widget, duration=500):

    end_pos = widget.pos()

    start_pos = QPoint(
        end_pos.x(),
        end_pos.y() + 80
    )

    widget.move(start_pos)

    animation = QPropertyAnimation(widget, b"pos")

    animation.setDuration(duration)

    animation.setStartValue(start_pos)

    animation.setEndValue(end_pos)

    animation.setEasingCurve(QEasingCurve.OutCubic)

    animation.start()

    widget._slide_animation = animation

    return animation


# ==========================================================
# Button Click Animation
# ==========================================================

def button_press(button):

    animation = QPropertyAnimation(button, b"geometry")

    rect = button.geometry()

    animation.setDuration(120)

    animation.setStartValue(rect)

    animation.setEndValue(rect.adjusted(2, 2, -2, -2))

    animation.setEasingCurve(QEasingCurve.OutQuad)

    animation.start()

    button._click_animation = animation

    return animation


# ==========================================================
# Neon Shadow
# ==========================================================

def apply_glow(widget):

    shadow = QGraphicsDropShadowEffect(widget)

    shadow.setBlurRadius(35)

    shadow.setOffset(0)

    shadow.setColor(QColor("#00FF88"))

    widget.setGraphicsEffect(shadow)

    return shadow


# ==========================================================
# Soft Shadow
# ==========================================================

def apply_shadow(widget):

    shadow = QGraphicsDropShadowEffect(widget)

    shadow.setBlurRadius(18)

    shadow.setOffset(0, 4)

    shadow.setColor(QColor(0, 0, 0, 170))

    widget.setGraphicsEffect(shadow)

    return shadow


# ==========================================================
# Card Animation
# ==========================================================

def animate_card(widget):

    fade = fade_in(widget, 300)

    slide = slide_from_bottom(widget, 300)

    group = QParallelAnimationGroup(widget)

    group.addAnimation(fade)

    group.addAnimation(slide)

    group.start()

    widget._card_group = group

    return group


# ==========================================================
# Window Animation
# ==========================================================

def animate_window(widget):

    fade = fade_in(widget, 500)

    slide = slide_from_left(widget, 500)

    group = QParallelAnimationGroup(widget)

    group.addAnimation(fade)

    group.addAnimation(slide)

    group.start()

    widget._window_group = group

    return group
