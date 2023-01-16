import React, { Component } from 'react';
import { Button, View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import Dialog, {
    DialogTitle,
    DialogContent,
    DialogFooter,
    DialogButton,
    SlideAnimation,
    ScaleAnimation,
} from 'react-native-popup-dialog';

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#696969',
    },
    dialogContentView: {
        // flex: 1,
        paddingLeft: 18,
        paddingRight: 18,
        // backgroundColor: '#000',
        // opacity: 0.4,
        // alignItems: 'center',
        // justifyContent: 'center',
    },
    navigationBar: {
        borderBottomColor: '#b5b5b5',
        borderBottomWidth: 0.5,
        backgroundColor: '#507d2a',
    },
    navigationTitle: {
        padding: 10,
    },
    navigationButton: {
        padding: 10,
        backgroundColor: '#507d2a',
    },
    navigationLeftButton: {
        paddingLeft: 20,
        paddingRight: 40,
    },
    navigator: {
        flex: 1,
        // backgroundColor: '#000000',
    },
    button: {
        alignItems: 'center',
        justifyContent: 'center',
        paddingVertical: 12,
        paddingHorizontal: 32,
        borderRadius: 4,
        elevation: 3,
        backgroundColor: 'white',
    },
    start: {
        fontSize: 16,
        lineHeight: 21,
        fontWeight: 'bold',
        letterSpacing: 0.25,
        color: 'black',
    },

});

export default class App extends Component {
    state = {

        scaleAnimationDialog: false,

    };

    render() {
        return (
            <View style={{ flex: 1 }}>
                <View style={styles.container}>
                    <TouchableOpacity style={styles.button} onPress={() => {
                        this.setState({
                            scaleAnimationDialog: true,
                        });
                    }}>
                        <Text style={styles.start}>переход </Text>
                    </TouchableOpacity>



                </View>



                <Dialog
                    onTouchOutside={() => {
                        this.setState({ scaleAnimationDialog: false });
                    }}
                    width={0.9}
                    visible={this.state.scaleAnimationDialog}
                    dialogAnimation={new ScaleAnimation()}
                    dialogTitle={
                        <DialogTitle
                            title="Приветствую тебя,турист. Для старта скажи ты тут впервые? "
                            style={{
                                backgroundColor: '#F7F7F8',
                            }}
                            hasTitleBar={false}
                            align="left"
                        />
                    }
                    actions={[
                        <DialogButton
                            text="DISMISS"
                            onPress={() => {
                                this.setState({ scaleAnimationDialog: false });
                            }}
                            key="button-1"
                        />,
                    ]}
                    footer={
                        <DialogFooter>
                            <DialogButton
                                text="Нет"
                                bordered
                                onPress={() => {
                                    this.setState({ defaultAnimationDialog: false });
                                }}
                                key="button-1"
                            />
                            <DialogButton
                                text="Да"
                                bordered
                                onPress={() => {
                                    this.setState({ defaultAnimationDialog: false });
                                }}
                                key="button-2"
                            />
                        </DialogFooter>
                    }
                >

                </Dialog>




            </View>
        );
    }
}