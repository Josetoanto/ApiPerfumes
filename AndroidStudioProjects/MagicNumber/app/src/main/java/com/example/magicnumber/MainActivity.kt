package com.example.magicnumber

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.magicnumber.features.magicNumber.screen.MagicNumberScreen
import com.example.magicnumber.features.magicNumber.viewModel.MagicNumberViewModel
import com.example.magicnumber.ui.theme.MagicNumberTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MagicNumberTheme {
                val magicNumberViewModel = MagicNumberViewModel()
                MagicNumberScreen(magicNumberViewModel)
            }
        }
    }
}
