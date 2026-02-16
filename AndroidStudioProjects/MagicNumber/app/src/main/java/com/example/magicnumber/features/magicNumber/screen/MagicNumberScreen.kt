package com.example.magicnumber.features.magicNumber.screen

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.magicnumber.features.magicNumber.viewModel.MagicNumberViewModel

@Composable
fun MagicNumberScreen(
    viewModel: MagicNumberViewModel
) {
    val state by viewModel.state.collectAsState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {

        Text(
            text = "Adivina el número (1 - 100)",
            style = MaterialTheme.typography.headlineSmall
        )

        Spacer(modifier = Modifier.height(16.dp))

        OutlinedTextField(
            value = state.userInput,
            onValueChange = {
                viewModel.onEvent(
                    MagicNumberViewModel.Event.OnInputChange(it)
                )
            },
            label = { Text("Número") }
        )

        Spacer(modifier = Modifier.height(16.dp))

        Button(
            onClick = {
                viewModel.onEvent(
                    MagicNumberViewModel.Event.OnCheckNumber
                )
            }
        ) {
            Text("Probar")
        }

        Spacer(modifier = Modifier.height(16.dp))

        Text(text = state.message)

        if (state.gameFinished) {
            Spacer(modifier = Modifier.height(24.dp))

            Button(
                onClick = {
                    viewModel.onEvent(
                        MagicNumberViewModel.Event.OnRestart
                    )
                }
            ) {
                Text("Reiniciar juego")
            }
        }
    }
}


