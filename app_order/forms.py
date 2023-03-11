from django import forms
from django.forms import TextInput, EmailInput, PasswordInput
from app_cart.models import User


# class OrderCustomerForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('password1', 'password2', 'full_name', 'email', 'phoneNumber')
#
#         widgets = {
#             'full_name': TextInput(attrs={'class': 'form-input',
#                                           'name': 'name',
#                                           'placeholder': 'Enter fullname',
#                                           }
#                                    ),
#             'email': EmailInput(attrs={'class': 'form-input',
#                                        'name': 'mail',
#                                        'placeholder': 'Enter e-mail',
#                                        }
#                                 ),
#             'phoneNumber': TextInput(attrs={'class': 'form-input',
#                                             'name': 'phone',
#                                             'placeholder': 'Enter phone',
#                                             }
#                                      ),
#
#             # 'password1': PasswordInput(attrs={'class': 'form-input',
#             #                                   'name': 'password',
#             #                                   'placeholder': 'Enter password',
#             #                                   }
#             #                            ),
#             #
#             # 'password2': PasswordInput(attrs={'class': 'form-input',
#             #                                   'name': 'passwordReply',
#             #                                   'placeholder': 'Enter password again',
#             #                                   }
#             #                            ),
#         }
