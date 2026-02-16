package com.example.magicnumber.features.magicNumber.viewModel

import androidx.compose.remote.creation.compose.state.abs
import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.update

class MagicNumberViewModel : ViewModel() {

    // ---------------- UDF STATE ----------------
    data class State(
        val targetNumber: Int = (1..100).random(),
        val userInput: String = "",
        val message: String = "",
        val gameFinished: Boolean = false
    )

    // ---------------- UDF EVENTS ----------------
    sealed interface Event {
        data class OnInputChange(val value: String) : Event
        object OnCheckNumber : Event
        object OnRestart : Event
    }

    private val _state = MutableStateFlow(State())
    val state: StateFlow<State> = _state

    // ---------------- EVENT HANDLER ----------------
    fun onEvent(event: Event) {
        when (event) {
            is Event.OnInputChange -> {
                _state.update { it.copy(userInput = event.value) }
            }

            Event.OnCheckNumber -> {
                evaluateNumber()
            }

            Event.OnRestart -> {
                restartGame()
            }
        }
    }

    // ---------------- BUSINESS LOGIC ----------------
    private fun evaluateNumber() {
        val input = _state.value.userInput.toIntOrNull() ?: return
        val target = _state.value.targetNumber
        val distance = abs(input - target)
        
        val resultMessage = when {
            input == target ->
                "🎉 Número adivinado. ¡Felicidades!"

            input < target && distance > 10 ->
                "Lejos y menor que"

            input < target && distance <= 10 ->
                "Cerca y menor que"

            distance <= 10 ->
                "Cerca y mayor que"

            else ->
                "Lejos y mayor que"
        }

        _state.update {
            it.copy(
                message = resultMessage,
                gameFinished = input == target
            )
        }
    }

    private fun restartGame() {
        _state.value = State()
    }
}
